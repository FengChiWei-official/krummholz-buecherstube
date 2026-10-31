"""vault_mcp: the vault's retrieval verbs over MCP, for agents with no shell.

The measured failure this server exists for: an agent whose tool set has no
bash/exec cannot run `vault.py retrieve`, and silently falls back to grep — the
degradation the docs forbid. So the contract under test is not just "it answers",
it is "it answers with exactly what the CLI would have printed".
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

from conftest import FIXTURE, REPO, TOOLS, run_vault

SERVER = TOOLS / "vault_mcp.py"

INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "test", "version": "0"}}}


def session(vault_root, *messages):
    """One server process; a `str` message is sent verbatim, a dict as JSON."""
    env = dict(os.environ, VAULT_ROOT=str(vault_root))
    payload = "".join(m if isinstance(m, str) else json.dumps(m) + "\n"
                      for m in messages)
    proc = subprocess.run([sys.executable, str(SERVER)], input=payload,
                          capture_output=True, text=True, env=env, cwd=str(REPO))
    assert proc.returncode == 0, proc.stderr
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


def call(tool, mid=7, **arguments):
    return {"jsonrpc": "2.0", "id": mid, "method": "tools/call",
            "params": {"name": tool, "arguments": arguments}}


def text_of(response) -> str:
    return response["result"]["content"][0]["text"]


def test_initialize_reports_the_server_and_the_negotiated_protocol():
    (response,) = session(FIXTURE, INIT)
    result = response["result"]
    assert result["protocolVersion"] == "2025-06-18"
    assert result["serverInfo"]["name"] == "vault"
    assert "tools" in result["capabilities"]


def test_an_unknown_protocol_version_falls_back_to_the_supported_one():
    """A client we do not know must still get an answer, not a silent hang."""
    (response,) = session(FIXTURE, {**INIT, "params": {"protocolVersion": "1999-01-01"}})
    assert response["result"]["protocolVersion"] == "2025-06-18"


def test_tools_list_exposes_the_two_retrieval_verbs():
    (response,) = session(FIXTURE, {**INIT, "id": 2, "method": "tools/list"})
    tools = {tool["name"]: tool for tool in response["result"]["tools"]}
    assert set(tools) == {"retrieve", "place"}
    assert tools["retrieve"]["inputSchema"]["required"] == ["term"]
    assert tools["place"]["inputSchema"]["required"] == ["name"]


def test_retrieve_returns_what_the_cli_prints():
    """Same config, same graph, same rendering — the CLI stays the contract."""
    (response,) = session(FIXTURE, call("retrieve", term="Node", n=5))
    assert response["result"]["isError"] is False
    assert text_of(response) == run_vault(FIXTURE, "retrieve", "Node", "--n", "5").stdout.rstrip("\n")


def test_place_reports_the_registration_edge():
    (response,) = session(FIXTURE, call("place", name="Node A"))
    text = text_of(response)
    assert "登记于 1 条边: Raw Index of Alpha" in text


def test_a_search_with_no_hits_is_an_answer_not_an_error():
    """The CLI exits 1 there; over MCP the text carries it and `isError` stays false."""
    (response,) = session(FIXTURE, call("retrieve", term="zzzznotfound"))
    assert response["result"]["isError"] is False
    assert "没有命中" in text_of(response)


def test_notifications_get_no_reply():
    responses = session(FIXTURE,
                        {"jsonrpc": "2.0", "method": "notifications/initialized"},
                        {**INIT, "id": 2, "method": "tools/list"})
    assert [r["id"] for r in responses] == [2]


def test_unknown_tool_and_unknown_method_are_errors():
    responses = session(FIXTURE, call("nope"), {**INIT, "id": 8, "method": "bogus/method"})
    assert [r["error"]["code"] for r in responses] == [-32602, -32601]


def test_a_parse_error_is_reported_and_the_session_survives():
    responses = session(FIXTURE, "not json at all\n", {**INIT, "id": 2, "method": "tools/list"})
    assert [r["error"]["code"] for r in responses if "error" in r] == [-32700]
    assert [r["id"] for r in responses if "result" in r] == [2]
