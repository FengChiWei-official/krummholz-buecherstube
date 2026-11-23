"""Offline tests for `.agent/skills/vault-images/r2put.py` against a mock R2 endpoint."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
MODULE = REPO / ".agent" / "skills" / "vault-images" / "r2put.py"
SVG = (b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
       b'<rect width="10" height="10"/></svg>')


def _load():
    spec = importlib.util.spec_from_file_location("r2put", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


r2put = _load()


@pytest.fixture()
def fake_r2():
    """A local server that behaves like the S3 PUT/HEAD surface r2put uses."""
    store = {"objects": {}, "headers": []}

    class Handler(BaseHTTPRequestHandler):
        def do_PUT(self):
            body = self.rfile.read(int(self.headers.get("content-length", 0)))
            assert hashlib.sha256(body).hexdigest() == self.headers["x-amz-content-sha256"]
            assert self.headers["Authorization"].startswith("AWS4-HMAC-SHA256 Credential=AK/")
            store["headers"].append({key.lower(): value
                                     for key, value in self.headers.items()})
            store["objects"][self.path] = (body, self.headers.get("content-type"))
            self.send_response(200)
            self.send_header("ETag", '"test"')
            self.end_headers()

        def do_HEAD(self):
            exists = self.path == "/my-books-asset" or self.path in store["objects"]
            self.send_response(200 if exists else 404)
            self.end_headers()

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}", store
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.fixture()
def env(monkeypatch, fake_r2, tmp_path):
    """Fully configured environment pointing at the mock; env file absent on purpose."""
    base_url, store = fake_r2
    for key, value in {
        "R2_ACCOUNT_ID": "acct",
        "R2_ACCESS_KEY_ID": "AK",
        "R2_SECRET_ACCESS_KEY": "SK",
        "R2_BUCKET": "my-books-asset",
        "R2_PUBLIC_BASE": "https://cdn.example",
        "R2_ENDPOINT": base_url,
    }.items():
        monkeypatch.setenv(key, value)
    for key in ("R2_PREFIX", "R2_SESSION_TOKEN"):
        monkeypatch.delenv(key, raising=False)
    return ["--env-file", str(tmp_path / "absent.env")], store


def test_selftest_matches_the_aws_vector(tmp_path, capsys):
    assert r2put.main(["--env-file", str(tmp_path / "absent.env"), "selftest"]) == 0
    assert "SigV4 vector matches" in capsys.readouterr().out


def test_put_svg_is_content_addressed_and_deduped(env, tmp_path, capsys):
    args, store = env
    figure = tmp_path / "figure.svg"
    figure.write_bytes(SVG)

    assert r2put.main([*args, "put", str(figure)]) == 0
    out = capsys.readouterr().out
    assert "uploaded  images/" in out
    assert "![](https://cdn.example/images/" in out
    assert len(store["objects"]) == 1
    path, (body, content_type) = next(iter(store["objects"].items()))
    assert path.startswith("/my-books-asset/images/") and path.endswith(".svg")
    assert body == SVG
    assert content_type == "image/svg+xml"

    assert r2put.main([*args, "put", str(figure)]) == 0
    assert "exists  images/" in capsys.readouterr().out
    assert len(store["objects"]) == 1


def test_put_pdf_lands_in_files_prefix_with_a_link_embed(env, tmp_path, capsys):
    args, store = env
    book = tmp_path / "book.pdf"
    book.write_bytes(b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\n")

    assert r2put.main([*args, "put", str(book)]) == 0
    out = capsys.readouterr().out
    assert "uploaded  files/" in out
    assert "[book.pdf](https://cdn.example/files/" in out
    path, (_body, content_type) = next(iter(store["objects"].items()))
    assert path.startswith("/my-books-asset/files/") and path.endswith(".pdf")
    assert content_type == "application/pdf"


def test_unknown_extension_requires_any(env, tmp_path, capsys):
    args, store = env
    note = tmp_path / "note.txt"
    note.write_bytes(b"hello\n")

    assert r2put.main([*args, "put", str(note)]) == 1
    assert "not an image or asset type" in capsys.readouterr().err
    assert store["objects"] == {}

    assert r2put.main([*args, "put", "--any", str(note)]) == 0
    assert "uploaded  files/" in capsys.readouterr().out
    path, (_body, content_type) = next(iter(store["objects"].items()))
    assert path.startswith("/my-books-asset/files/")
    assert content_type == "application/octet-stream"


def test_dry_run_needs_no_config(tmp_path, monkeypatch, capsys):
    for key in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY",
                "R2_BUCKET", "R2_PUBLIC_BASE", "R2_PREFIX", "R2_ENDPOINT",
                "R2_SESSION_TOKEN"):
        monkeypatch.delenv(key, raising=False)
    figure = tmp_path / "draft.svg"
    figure.write_bytes(SVG)

    args = ["--env-file", str(tmp_path / "absent.env")]
    assert r2put.main([*args, "put", "--dry-run", str(figure)]) == 0
    assert "dry-run  images/" in capsys.readouterr().out


def test_check_accepts_a_bare_host_public_base(env, monkeypatch, tmp_path, capsys):
    """`R2_PUBLIC_BASE` written as a bare custom domain still yields https links."""
    args, _store = env
    monkeypatch.setenv("R2_PUBLIC_BASE", "cdn.example/")

    assert r2put.main([*args, "check"]) == 0
    out = capsys.readouterr().out
    assert "ok  bucket my-books-asset reachable, credentials accepted" in out
    assert "public   https://cdn.example" in out

    figure = tmp_path / "figure.svg"
    figure.write_bytes(SVG)
    assert r2put.main([*args, "put", str(figure)]) == 0
    assert "![](https://cdn.example/images/" in capsys.readouterr().out


def test_presign_signs_and_clamps_expiry(env, capsys):
    args, _store = env

    def sign(expires):
        assert r2put.main([*args, "presign", "files/probe.txt",
                           "--method", "PUT", "--expires", str(expires)]) == 0
        return capsys.readouterr().out.strip()

    url = sign(3600)
    assert "X-Amz-Algorithm=AWS4-HMAC-SHA256" in url
    assert "X-Amz-SignedHeaders=host" in url
    assert "X-Amz-Expires=3600" in url
    assert re.search(r"X-Amz-Signature=[0-9a-f]{64}$", url)
    assert "X-Amz-Expires=1&" in sign(0)
    assert "X-Amz-Expires=604800&" in sign(999999)


def test_session_token_is_signed(env, monkeypatch, tmp_path, capsys):
    args, store = env
    monkeypatch.setenv("R2_SESSION_TOKEN", "tok")
    figure = tmp_path / "figure.svg"
    figure.write_bytes(SVG)

    assert r2put.main([*args, "put", str(figure)]) == 0
    capsys.readouterr()
    headers = store["headers"][-1]
    assert headers["x-amz-security-token"] == "tok"
    assert "x-amz-security-token" in headers["authorization"]
