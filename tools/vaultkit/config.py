"""Config loading — zones, genres, thresholds, paths and baselines.

The single home for every tunable is `tools/vault.toml`; no zone name, genre
prefix or threshold is written into the code. Vault root resolution:

    explicit --vault > $VAULT_ROOT > repo root (parent of tools/)
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
TOOLS_DIR = PKG_DIR.parent
REPO_ROOT = TOOLS_DIR.parent
CONFIG_PATH = TOOLS_DIR / "vault.toml"

ENV_VAULT_ROOT = "VAULT_ROOT"


class ConfigError(RuntimeError):
    """A required config file is missing or unreadable."""


def _load_extra_lines(path: Path) -> set:
    """Read one-entry-per-line file, skipping blanks and # comments."""
    if not path.exists():
        return set()
    result = set()
    for line in path.read_text().splitlines():
        line = line.strip().split("#")[0].strip()
        if line:
            result.add(line)
    return result


@dataclass(frozen=True)
class Config:
    root: Path
    zones: dict
    genres: dict
    thresholds: dict
    paths: dict
    skip_dirs: frozenset
    notes_skip_dirs: frozenset
    root_allowed: frozenset
    trunk_root_stem: str
    trunk_model: str
    baseline_lit_nosource_stems: frozenset
    whitelist_unresolved: frozenset
    source: Path

    # -- path helpers (all relative to the vault root) --------------------
    def under(self, key: str) -> Path:
        return self.root / self.paths[key]

    @property
    def library(self) -> Path:
        return self.under("library")

    @property
    def material_dir(self) -> Path:
        return self.under("archives_material")

    @property
    def todos_dir(self) -> Path:
        return self.under("todos")

    @property
    def doctrine_dir(self) -> Path:
        return self.under("doctrine")

    @property
    def zzz_dir(self) -> Path:
        return self.under("zzz")

    @property
    def raw_dir(self) -> Path:
        return self.library / self.zones["raw"]

    @property
    def links_dir(self) -> Path:
        return self.library / self.zones["links"]

    # -- genre / zone (doctrine: name > path) ------------------------------
    def genre(self, stem: str) -> str:
        g = self.genres
        if stem.startswith(g["raw_prefix"]):
            return "raw"
        if stem.startswith(g["index_prefix"]) or stem.endswith(g["index_suffix"]):
            return "index"
        if stem.startswith(g["links_prefix"]):
            return "links"
        return "node"

    def zone(self, path: Path) -> str | None:
        """library sub-zone: Raw / Index / Links / <fold>, else None."""
        try:
            rel = path.relative_to(self.root)
        except ValueError:
            return None
        parts = rel.parts
        if parts[0] != self.paths["library"] or len(parts) < 3:
            return None
        return parts[1]


def resolve_root(explicit: str | Path | None = None) -> Path:
    """Vault root: explicit argument, then $VAULT_ROOT, then the repo root."""
    if explicit:
        return Path(explicit).resolve()
    env = os.environ.get(ENV_VAULT_ROOT)
    if env:
        return Path(env).resolve()
    return REPO_ROOT


def load(root: str | Path | None = None, config_path: Path | None = None) -> Config:
    path = Path(config_path) if config_path else CONFIG_PATH
    if not path.exists():
        raise ConfigError(f"missing config {path}")
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"unreadable config {path}: {exc}") from exc

    vault_root = resolve_root(root)
    zones = dict(data["zones"])
    genres = dict(data["genres"])
    thresholds = {k: v for k, v in data["thresholds"].items()}
    paths = dict(data["paths"])
    skip_dirs = frozenset(data["scan"]["skip_dirs"])
    notes_skip_dirs = skip_dirs | frozenset(data["scan"]["notes_extra_skip_dirs"])

    baseline = set(data["baseline"]["lit_nosource_stems"])
    for entry in _load_extra_lines(vault_root / data["files"]["baseline_lit_nosource"]):
        baseline.add(Path(entry).stem)
    whitelist = _load_extra_lines(vault_root / data["files"]["whitelist_unresolved"])

    return Config(
        root=vault_root,
        zones=zones,
        genres=genres,
        thresholds=thresholds,
        paths=paths,
        skip_dirs=skip_dirs,
        notes_skip_dirs=notes_skip_dirs,
        root_allowed=frozenset(data["scan"]["root_allowed"]),
        trunk_root_stem=data["trunk"]["root_stem"],
        trunk_model=data["trunk"]["model"],
        baseline_lit_nosource_stems=frozenset(baseline),
        whitelist_unresolved=frozenset(whitelist),
        source=path,
    )
