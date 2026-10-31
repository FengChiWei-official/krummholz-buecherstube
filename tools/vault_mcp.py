#!/usr/bin/env python3
"""vault_mcp — the vault's retrieval verbs over MCP stdio, so no shell is needed.

    python3 tools/vault_mcp.py        # MCP server on stdin/stdout

Why it exists: an agent whose tool set has no bash/exec cannot run
`vault.py retrieve`, so it silently falls back to grep — the degradation the
docs forbid ("never the opening move"). This server gives such an agent the same
verb, with the same config, the same `Graph` and the same rendering as the CLI
(P2 single parser / P3 single config / P8 output-as-contract): the tool result is
byte-for-byte what `vault.py retrieve` prints.

Tools: `retrieve TERM [n]`, `place NAME`. Every call re-reads the vault
(~0.2 s at ~1.3k notes), so an answer is never stale. `$VAULT_ROOT` is honoured
exactly like the CLI. A search with no hits is an answer, not a failure — the
result carries the text and `isError` stays false; only an exception sets it.

Wire it into an MCP client with command `python3`, args `tools/vault_mcp.py`,
cwd = the vault root (`doctrine/New Machine.md` §步骤 7).
"""

from __future__ import annotations

import contextlib
import io
import json
import signal
import sys
from argparse import Namespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vaultkit import __version__, model  # noqa: E402
from vaultkit.cli import cmd_place, cmd_retrieve, load_config  # noqa: E402

PROTOCOL_VERSION = "2025-06-18"
KNOWN_PROTOCOL_VERSIONS = {"2025-06-18", "2025-03-26", "2024-11-05", "2024-10-07"}
SERVER_INFO = {"name": "vault", "version": __version__}

TOOLS = [
    {
        "name": "retrieve",
        "description": (
            "Whole-vault retrieval ranked by the vault's own evidence (name / "
            "alias / registration / Index area / text / shared neighbour), one "
            "why-line per hit, each hit with its registrations, areas and role. "
            "This is the vault's `retrieve` verb — use it before grep. The match "
            "is literal and the vault is bilingual (中文 / English): try both "
            "forms before concluding there is no such note."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "term": {"type": "string", "description": "search term"},
                "n": {"type": "integer", "description": "max hits (default 15)"},
            },
            "required": ["term"],
            "additionalProperties": False,
        },
    },
    {
        "name": "place",
        "description": (
            "Where one note sits in the relation graph: its registration edges "
            "(which Raw Index registers it), the 归队 proposals with the voting "
            "evidence, its Index areas, out/in links, and the notes worth linking "
            "first. Read-only, like the CLI verb of the same name."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "note name or alias"},
            },
            "required": ["name"],
            "additionalProperties": False,
        },
    },
]

TOOL_NAMES = {tool["name"] for tool in TOOLS}


def _run_in_process(fn, args: Namespace) -> str:
    """Run one CLI command in-process; return exactly what it prints.

    Rendering is the CLI's own (`cmd_retrieve` / `cmd_place`), so this server
    cannot drift from `vault.py` output without the CLI tests going red first.
    """
    cfg = load_config(strict=False)
    for warning in cfg.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    graph = model.load(cfg)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(cfg, graph, args)
    return buf.getvalue().rstrip("\n")


def call_tool(name: str, arguments: dict) -> str:
    if name == "retrieve":
        n = arguments.get("n")
        return _run_in_process(
            cmd_retrieve,
            Namespace(term=str(arguments.get("term", "")),
                      n=15 if n is None else int(n), json=False))
    if name == "place":
        return _run_in_process(
            cmd_place, Namespace(name=str(arguments.get("name", "")), json=False))
    raise KeyError(name)


def _ok(mid, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def _err(mid, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}


def _call_tool(mid, params: dict) -> dict:
    name = params.get("name")
    arguments = params.get("arguments") or {}
    if name not in TOOL_NAMES:
        return _err(mid, -32602, f"unknown tool: {name}")
    if not isinstance(arguments, dict):
        return _err(mid, -32602, "`arguments` must be an object")
    try:
        text = call_tool(name, arguments)
    except Exception as exc:  # noqa: BLE001 — a tool failure is a result, not a crash
        return _ok(mid, {"content": [{"type": "text",
                                      "text": f"{type(exc).__name__}: {exc}"}],
                         "isError": True})
    return _ok(mid, {"content": [{"type": "text", "text": text}], "isError": False})


def handle(msg: dict) -> dict | None:
    """One MCP message in, one response out (`None` = notification, no reply)."""
    method = msg.get("method")
    if not isinstance(method, str) or "id" not in msg:
        return None  # a notification, or a response to something we never sent
    mid = msg.get("id")
    params = msg.get("params") if isinstance(msg.get("params"), dict) else {}
    if method == "initialize":
        requested = params.get("protocolVersion")
        version = requested if requested in KNOWN_PROTOCOL_VERSIONS else PROTOCOL_VERSION
        return _ok(mid, {"protocolVersion": version,
                         "capabilities": {"tools": {"listChanged": False}},
                         "serverInfo": SERVER_INFO})
    if method == "ping":
        return _ok(mid, {})
    if method == "tools/list":
        return _ok(mid, {"tools": TOOLS})
    if method == "tools/call":
        return _call_tool(mid, params)
    return _err(mid, -32601, f"method not found: {method}")


def serve(stdin, stdout) -> int:
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            response = _err(None, -32700, "parse error")
        else:
            if not isinstance(msg, dict):
                response = _err(None, -32700, "message must be a JSON object")
            else:
                response = handle(msg)
        if response is None:
            continue
        stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        stdout.flush()
    return 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("-h", "--help"):
        print((__doc__ or "").strip())
        return 0
    # Same rule as the CLI: a client that closes the protocol pipe ends this
    # process by SIGPIPE rather than a BrokenPipeError traceback.
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    return serve(sys.stdin, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
