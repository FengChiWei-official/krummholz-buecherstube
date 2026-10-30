#!/usr/bin/env python3
"""Thin entry point. Implementation lives in `tools/vaultkit/` (v6, plan P2).

    python3 tools/vault.py check
    python3 tools/vault.py triage
    python3 tools/vault.py status
    python3 tools/vault.py rawindex [--clusters] [--check] [--sync] [--around NAME] [--top N]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vaultkit.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
