"""Shared test setup: import the package, run the CLI against fixture vaults."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "mini_vault"

sys.path.insert(0, str(TOOLS))


@pytest.fixture()
def vault(tmp_path: Path) -> Path:
    """A throwaway copy of the fixture vault (tests may mutate it)."""
    dest = tmp_path / "mini_vault"
    shutil.copytree(FIXTURE, dest)
    return dest


@pytest.fixture()
def real_vault_root() -> Path:
    return FIXTURE


def run_vault(vault_root: Path, *args: str):
    """Run tools/vault.py with VAULT_ROOT pointed at `vault_root`."""
    env = dict(os.environ, VAULT_ROOT=str(vault_root))
    return subprocess.run([sys.executable, str(TOOLS / "vault.py"), *args],
                          capture_output=True, text=True, env=env, cwd=str(REPO))
