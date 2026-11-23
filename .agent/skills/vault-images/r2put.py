#!/usr/bin/env python3
"""r2put — host images and assets for the vault on a public Cloudflare R2 bucket.

The vault stays text-only: pictures and files live in R2, notes keep one URL.
Stdlib only (no boto3/aws cli), so it works on a bare machine.

Config, from the environment or an env file (default ~/.config/krummholz/r2.env,
each line KEY=VALUE; the environment wins):

    R2_ACCOUNT_ID         Cloudflare account id (endpoint: <id>.r2.cloudflarestorage.com)
    R2_ACCESS_KEY_ID      R2 API token access key id
    R2_SECRET_ACCESS_KEY  R2 API token secret
    R2_BUCKET             bucket name
    R2_PUBLIC_BASE        public base url, e.g. https://pub-xxxx.r2.dev or a custom domain
    R2_PREFIX             optional key prefix (default "images/" for images, "files/" for assets)
    R2_ENDPOINT           optional endpoint override (tests / custom gateway)
    R2_SESSION_TOKEN      optional temporary-credential token (x-amz-security-token)

Commands:
    check                 config present + credentials accepted (HeadBucket)
    put FILE [FILE ...]   upload; content-addressed key by default; prints url + markdown
    presign KEY           time-limited URL for a client that has no credentials
    selftest              verify the SigV4 signer against the AWS S3 published vector

Exit codes: 0 ok / 1 failure / 2 config missing.

The token read here is an R2 API token (S3 credentials: Access Key ID + Secret).
A Cloudflare management API token is a different thing and cannot sign S3 requests.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENV_KEYS = (
    "R2_ACCOUNT_ID",
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
    "R2_BUCKET",
    "R2_PUBLIC_BASE",
)
OPTIONAL_KEYS = ("R2_PREFIX", "R2_ENDPOINT", "R2_SESSION_TOKEN")
DEFAULT_ENV_FILE = Path.home() / ".config" / "krummholz" / "r2.env"
MAX_BYTES = 100 * 1024 * 1024
MAX_EXPIRES = 604800
REGION = "auto"
SERVICE = "s3"

IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".avif": "image/avif",
}
ASSET_TYPES = {
    ".pdf": "application/pdf",
    ".epub": "application/epub+zip",
}
ANY_TYPE = "application/octet-stream"

# ---------------------------------------------------------------- config


def _parse_env_file(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key.strip()] = value
    return out


def load_config(env_file: Path) -> dict:
    cfg = {key: "" for key in ENV_KEYS + OPTIONAL_KEYS}
    for key, value in _parse_env_file(env_file).items():
        if key in cfg:
            cfg[key] = value
    for key in cfg:  # an explicit environment value wins over the file
        env_value = os.environ.get(key, "")
        if env_value:
            cfg[key] = env_value
    return cfg


def missing_keys(cfg: dict, need_public: bool = True) -> list:
    keys = ENV_KEYS if need_public else tuple(k for k in ENV_KEYS if k != "R2_PUBLIC_BASE")
    return [key for key in keys if not cfg.get(key)]


def endpoint(cfg: dict) -> str:
    return (cfg.get("R2_ENDPOINT") or
            f"https://{cfg['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com").rstrip("/")


def public_base(cfg: dict) -> str:
    """The public read base as a full URL; a bare host means https."""
    base = (cfg.get("R2_PUBLIC_BASE") or "").strip().rstrip("/")
    if base and "://" not in base:
        base = "https://" + base
    return base


def public_url(cfg: dict, key: str) -> str:
    base = public_base(cfg)
    if not base:
        return ""
    return base + "/" + urllib.parse.quote(key, safe="/-_.~")


# ---------------------------------------------------------------- signing


def _hmac(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _signature(secret_key: str, amzdate: str, string_to_sign: str,
               region: str = REGION, service: str = SERVICE) -> str:
    key = _hmac(("AWS4" + secret_key).encode("utf-8"), amzdate[:8])
    key = _hmac(key, region)
    key = _hmac(key, service)
    key = _hmac(key, "aws4_request")
    return hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()


def sign_v4(
    method: str,
    host: str,
    canonical_uri: str,
    payload_sha: str,
    headers: dict,
    access_key: str,
    secret_key: str,
    amzdate: str,
    region: str = REGION,
    service: str = SERVICE,
    canonical_query: str = "",
) -> tuple:
    """Return (authorization header, canonical request, string to sign)."""
    signed_headers = ";".join(sorted(name.lower() for name in headers))
    canonical_headers = "".join(
        f"{name.lower()}:{' '.join(str(headers[name]).split())}\n"
        for name in sorted(headers, key=str.lower)
    )
    canonical_request = "\n".join(
        [method, canonical_uri, canonical_query, canonical_headers, signed_headers, payload_sha]
    )
    scope = f"{amzdate[:8]}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amzdate,
            scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )
    signature = _signature(secret_key, amzdate, string_to_sign, region, service)
    authorization = (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    return authorization, canonical_request, string_to_sign


def sign_request(cfg, method, key, body=b"", content_type=None, cache_control=None):
    base = endpoint(cfg)
    host = urllib.parse.urlsplit(base).netloc
    canonical_uri = "/" + cfg["R2_BUCKET"]
    if key:
        canonical_uri += "/" + urllib.parse.quote(key, safe="/-_.~")
    amzdate = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    payload_sha = hashlib.sha256(body).hexdigest()
    headers = {
        "host": host,
        "x-amz-content-sha256": payload_sha,
        "x-amz-date": amzdate,
    }
    if cfg.get("R2_SESSION_TOKEN"):
        headers["x-amz-security-token"] = cfg["R2_SESSION_TOKEN"]
    if content_type:
        headers["content-type"] = content_type
    if cache_control:
        headers["cache-control"] = cache_control
    authorization, _, _ = sign_v4(
        method,
        host,
        canonical_uri,
        payload_sha,
        headers,
        cfg["R2_ACCESS_KEY_ID"],
        cfg["R2_SECRET_ACCESS_KEY"],
        amzdate,
    )
    send = {name: value for name, value in headers.items() if name != "host"}
    send["Authorization"] = authorization
    url = base + canonical_uri
    return url, send, payload_sha


def call(cfg, method, key=None, body=b"", content_type=None, cache_control=None):
    url, headers, _ = sign_request(cfg, method, key, body, content_type, cache_control)
    request = urllib.request.Request(url, data=body if method == "PUT" else None,
                                     headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()
    except urllib.error.URLError as error:
        raise SystemExit(f"r2put: network error: {error.reason}")


def presign_url(cfg, key: str, method: str = "GET", expires: int = 3600) -> str:
    """Sign a URL that a client without credentials can PUT/GET for `expires` seconds."""
    expires = max(1, min(MAX_EXPIRES, int(expires)))
    base = endpoint(cfg)
    host = urllib.parse.urlsplit(base).netloc
    amzdate = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    scope = f"{amzdate[:8]}/{REGION}/{SERVICE}/aws4_request"
    path = "/" + cfg["R2_BUCKET"] + "/" + urllib.parse.quote(key.lstrip("/"), safe="/-_.~")
    params = {
        "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
        "X-Amz-Credential": f"{cfg['R2_ACCESS_KEY_ID']}/{scope}",
        "X-Amz-Date": amzdate,
        "X-Amz-Expires": str(expires),
        "X-Amz-SignedHeaders": "host",
    }
    if cfg.get("R2_SESSION_TOKEN"):
        params["X-Amz-Security-Token"] = cfg["R2_SESSION_TOKEN"]
    encoded = sorted(
        (urllib.parse.quote(name, safe="-_.~"), urllib.parse.quote(value, safe="-_.~"))
        for name, value in params.items()
    )
    canonical_query = "&".join(f"{name}={value}" for name, value in encoded)
    canonical_request = "\n".join(
        [method, path, canonical_query, f"host:{host}\n", "host", "UNSIGNED-PAYLOAD"]
    )
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amzdate,
            scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )
    signature = _signature(cfg["R2_SECRET_ACCESS_KEY"], amzdate, string_to_sign)
    return f"{base}{path}?{canonical_query}&X-Amz-Signature={signature}"


# ---------------------------------------------------------------- payload


def sniff(path: Path, allow_any: bool = False) -> tuple:
    """Return (kind, suffix, content-type) or raise ValueError for a rejected file."""
    suffix = path.suffix.lower()
    if suffix in IMAGE_TYPES:
        head = path.read_bytes()[:512]
        lowered = head.lower()
        ok = {
            ".png": head.startswith(b"\x89PNG\r\n\x1a\n"),
            ".jpg": head.startswith(b"\xff\xd8\xff"),
            ".jpeg": head.startswith(b"\xff\xd8\xff"),
            ".gif": lowered.startswith(b"gif87a") or lowered.startswith(b"gif89a"),
            ".webp": head[:4] == b"RIFF" and head[8:12] == b"WEBP",
            ".svg": b"<svg" in lowered,
            ".avif": head[4:8] == b"ftyp",
        }[suffix]
        if not ok:
            raise ValueError(f"{path.name}: content does not look like {suffix}")
        return "image", suffix, IMAGE_TYPES[suffix]
    if suffix in ASSET_TYPES:
        head = path.read_bytes()[:512]
        marker = b"%PDF-" if suffix == ".pdf" else b"PK\x03\x04"
        if not head.startswith(marker):
            raise ValueError(f"{path.name}: content does not look like {suffix}")
        return "asset", suffix, ASSET_TYPES[suffix]
    if allow_any:
        return "other", suffix, ANY_TYPE
    raise ValueError(f"{path.name}: not an image or asset type (--any to override)")


def content_key(path: Path, cfg: dict, key: str | None,
                allow_any: bool = False) -> tuple:
    """Return (kind, key, content-type, sha256)."""
    kind, suffix, content_type = sniff(path, allow_any)
    if key:
        return kind, key.lstrip("/"), content_type, ""
    body = path.read_bytes()
    digest = hashlib.sha256(body).hexdigest()
    prefix = (cfg.get("R2_PREFIX") or ("images/" if kind == "image" else "files/")).strip("/")
    return kind, f"{prefix}/{digest[:20]}{suffix}", content_type, digest


# ---------------------------------------------------------------- commands


def cmd_check(cfg) -> int:
    missing = missing_keys(cfg)
    if missing:
        print("r2put: missing config: " + ", ".join(missing))
        print(f"r2put: put them in {DEFAULT_ENV_FILE} (KEY=VALUE, mode 600) or the environment")
        return 2
    status, body = call(cfg, "HEAD")
    if status in (200, 204, 301):
        print(f"ok  bucket {cfg['R2_BUCKET']} reachable, credentials accepted")
        print(f"    endpoint {endpoint(cfg)}")
        print(f"    public   {public_base(cfg)}")
        if "r2.dev" in cfg["R2_PUBLIC_BASE"]:
            print("note  r2.dev 公开域名有速率限制；长期链接建议绑定自定义域")
        return 0
    detail = body[:300].decode("utf-8", "replace")
    print(f"r2put: HeadBucket failed: HTTP {status} {detail.strip()}")
    if status == 403:
        print("r2put: token lacks Object Read/Write or the account id / bucket is wrong")
    if status == 404:
        print("r2put: no such bucket")
    return 1


def cmd_put(cfg, files, args) -> int:
    missing = missing_keys(cfg)
    if missing and not args.dry_run:
        print("r2put: missing config: " + ", ".join(missing), file=sys.stderr)
        return 2
    if missing:
        print("r2put: dry-run without config; key only, no url: "
              + ", ".join(missing), file=sys.stderr)
    results = []
    failed = 0
    for name in files:
        path = Path(name)
        try:
            if not path.is_file():
                raise ValueError(f"{name}: no such file")
            size = path.stat().st_size
            if size > args.max_bytes:
                raise ValueError(f"{name}: {size} bytes > limit {args.max_bytes}")
            kind, key, content_type, digest = content_key(path, cfg, args.key, args.any)
        except ValueError as error:
            print(f"r2put: {error}", file=sys.stderr)
            failed += 1
            continue
        url = public_url(cfg, key)
        if args.dry_run:
            results.append({"file": str(path), "key": key, "url": url, "kind": kind,
                            "bytes": size, "content_type": content_type,
                            "uploaded": False, "dry_run": True})
            continue
        if not args.no_dedupe:
            status, _ = call(cfg, "HEAD", key)
            if status == 200:
                results.append({"file": str(path), "key": key, "url": url, "kind": kind,
                                "bytes": size, "content_type": content_type,
                                "uploaded": False})
                continue
        body = path.read_bytes()
        cache = "public, max-age=31536000, immutable" if not args.key else None
        status, detail = call(cfg, "PUT", key, body, content_type, cache)
        if status not in (200, 201):
            print(f"r2put: PUT {key} failed: HTTP {status} "
                  f"{detail[:300].decode('utf-8', 'replace').strip()}", file=sys.stderr)
            failed += 1
            continue
        results.append({"file": str(path), "key": key, "url": url, "kind": kind,
                        "bytes": size, "content_type": content_type, "uploaded": True,
                        "sha256": digest or None})

    if args.json:
        print(json.dumps({"results": results}, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        for item in results:
            mark = "uploaded" if item.get("uploaded") else (
                "dry-run" if item.get("dry_run") else "exists")
            print(f"{mark}  {item['key']}  ({item['bytes']} B)")
            if item["url"]:
                print(f"  {item['url']}")
                if item["kind"] == "image":
                    print(f"  ![]({item['url']})")
                else:
                    print(f"  [{Path(item['file']).name}]({item['url']})")
    return 1 if failed else 0


def cmd_presign(cfg, key, args) -> int:
    missing = missing_keys(cfg, need_public=False)
    if missing:
        print("r2put: missing config: " + ", ".join(missing), file=sys.stderr)
        return 2
    url = presign_url(cfg, key, args.method, args.expires)
    print(json.dumps({"url": url}) if args.json else url)
    return 0


# AWS documents this request ("Signature Calculation Examples: GET Object"):
# GET /test.txt on examplebucket, us-east-1, 20130524T000000Z, Range: bytes=0-9.
SELFTEST = dict(
    method="GET",
    host="examplebucket.s3.amazonaws.com",
    canonical_uri="/test.txt",
    payload_sha="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    headers={
        "host": "examplebucket.s3.amazonaws.com",
        "range": "bytes=0-9",
        "x-amz-content-sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "x-amz-date": "20130524T000000Z",
    },
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    amzdate="20130524T000000Z",
    region="us-east-1",
    expect="f0e8bdb87c964420e857bd35b5d6ed310bd44f0170aba48dd91039c6036bdb41",
)


def cmd_selftest(_cfg) -> int:
    authorization, canonical_request, string_to_sign = sign_v4(
        SELFTEST["method"], SELFTEST["host"], SELFTEST["canonical_uri"],
        SELFTEST["payload_sha"], dict(SELFTEST["headers"]), SELFTEST["access_key"],
        SELFTEST["secret_key"], SELFTEST["amzdate"], SELFTEST["region"])
    got = authorization.rsplit("Signature=", 1)[1]
    if got == SELFTEST["expect"]:
        print(f"ok  SigV4 vector matches ({got[:16]}…)")
        return 0
    print("r2put: SigV4 selftest FAILED", file=sys.stderr)
    print(f"  expected {SELFTEST['expect']}", file=sys.stderr)
    print(f"  got      {got}", file=sys.stderr)
    print("  canonical request:", file=sys.stderr)
    print(canonical_request, file=sys.stderr)
    print("  string to sign:", file=sys.stderr)
    print(string_to_sign, file=sys.stderr)
    return 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="r2put", description="Host images and assets for the vault on Cloudflare R2.")
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--json", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="verify config and credentials")
    put = sub.add_parser("put", help="upload files")
    put.add_argument("files", nargs="+")
    put.add_argument("--key", help="explicit object key (default: content-addressed)")
    put.add_argument("--no-dedupe", action="store_true", help="upload even if the key exists")
    put.add_argument("--dry-run", action="store_true")
    put.add_argument("--any", action="store_true",
                     help="accept any extension as application/octet-stream")
    put.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    presign = sub.add_parser("presign", help="print a time-limited URL")
    presign.add_argument("key")
    presign.add_argument("--method", choices=("PUT", "GET"), default="GET")
    presign.add_argument("--expires", type=int, default=3600)
    sub.add_parser("selftest", help="verify the SigV4 signer")
    args = parser.parse_args(argv)

    cfg = load_config(args.env_file)
    if args.command == "check":
        return cmd_check(cfg)
    if args.command == "put":
        return cmd_put(cfg, args.files, args)
    if args.command == "presign":
        return cmd_presign(cfg, args.key, args)
    if args.command == "selftest":
        return cmd_selftest(cfg)
    parser.error("unknown command")


if __name__ == "__main__":
    sys.exit(main())
