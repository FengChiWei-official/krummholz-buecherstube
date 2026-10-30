"""Model tests: zones, genres, registration edges and the shared graph."""

from __future__ import annotations

import pytest

from vaultkit import config, model

FIXTURE = config.REPO_ROOT / "tests" / "fixtures" / "mini_vault"


@pytest.fixture()
def cfg(tmp_path):
    return config.load(root=FIXTURE)


@pytest.fixture()
def graph(cfg):
    model.clear_cache()
    return model.load(cfg)


def test_zones_and_genres(cfg):
    lib = cfg.library
    assert cfg.zone(lib / "Raw" / "Raw Index of Alpha.md") == "Raw"
    assert cfg.zone(lib / "Index" / "Index of Alpha Area.md") == "Index"
    assert cfg.zone(lib / "Links" / "Links of A and B.md") == "Links"
    assert cfg.zone(lib / "A_fold" / "Node A.md") == "A_fold"
    assert cfg.zone(cfg.root / "README.md") is None

    assert cfg.genre("Raw Index of Alpha") == "raw"
    assert cfg.genre("Index of Alpha Area") == "index"
    assert cfg.genre("Alpha-MOC") == "index"
    assert cfg.genre("Links of A and B") == "links"
    assert cfg.genre("Node A") == "node"


def test_zone_membership(graph):
    stems = lambda paths: sorted(p.stem for p in paths)  # noqa: E731
    assert stems(graph.raws) == ["Raw Index of Alpha", "Raw Index of Beta",
                                "Raw Index of Everything"]
    assert stems(graph.idxs) == ["Alpha-MOC", "Index of Alpha Area", "Index of Beta Area"]
    assert stems(graph.linksn) == ["Links of A and B"]
    assert stems(graph.nodes) == ["Fence Node", "Node A", "Node B", "Node Shared", "Node Zero"]
    assert stems(graph.doctrine) == ["Vault Design"]


def test_registration_edges_are_unique_pairs(graph):
    edges = {(r.stem, n.stem) for r, n in graph.registration_edges}
    assert edges == {("Raw Index of Alpha", "Node A"),
                     ("Raw Index of Alpha", "Node Shared"),
                     ("Raw Index of Beta", "Node B"),
                     ("Raw Index of Beta", "Node Shared")}
    assert len(graph.registration_edges) == len(edges)


def test_multi_parent_registration_is_visible(graph):
    assert graph.multi_registered() == {"Node Shared": ["Raw Index of Alpha",
                                                       "Raw Index of Beta"]}
    assert sorted(n.stem for n in graph.unregistered()) == ["Fence Node", "Node Zero"]


def test_alias_resolution_in_graph(graph):
    node_a = graph.stems["Node A"]
    assert node_a in graph.out[graph.stems["Node B"]]


def test_code_fence_link_is_not_an_edge(graph):
    fence = graph.stems["Fence Node"]
    assert graph.out[fence] == set()
    assert fence in graph.zero_outlink()


def test_raw_index_chain_is_cycle_free(graph):
    everything = graph.stems["Raw Index of Everything"]
    alpha = graph.stems["Raw Index of Alpha"]
    beta = graph.stems["Raw Index of Beta"]
    assert alpha in graph.out[everything]
    assert beta in graph.out[alpha]
    assert everything not in graph.out[beta]


def test_links_note_crosses_two_areas(graph):
    links_note = graph.stems["Links of A and B"]
    members = [q for q in graph.out[links_note] if q in graph.area]
    areas = set().union(*[graph.area[q] for q in members])
    assert len(areas) >= 2


def test_graph_is_built_once_per_process(cfg):
    model.clear_cache()
    assert model.load(cfg) is model.load(cfg)


def test_config_has_no_hardcoded_thresholds():
    cfg = config.load(root=FIXTURE)
    assert cfg.thresholds["todo_stale_days"] == 90
    assert cfg.trunk_model == "tree"
    assert cfg.trunk_root_stem == "Raw Index of Everything"
    assert cfg.zones["node_suffix"] == "_fold"


def test_missing_config_raises(tmp_path):
    with pytest.raises(config.ConfigError):
        config.load(root=FIXTURE, config_path=tmp_path / "nope.toml")


def test_git_first_seen_index_is_one_pass_and_cached(tmp_path):
    from vaultkit import cli

    cli._FIRST_SEEN_CACHE.clear()
    real = config.load(root=config.REPO_ROOT)
    index = cli.git_first_seen_index(real)
    assert index, "expected the real repo to yield first-seen entries"
    assert isinstance(index["README.md"], float)
    assert cli.git_first_seen_index(real) is index          # cached, not re-shelled

    # A vault nested inside another repo reports repo-relative paths, so the
    # index must be refused rather than silently mis-keyed.
    cli._FIRST_SEEN_CACHE.clear()
    nested = config.load(root=FIXTURE)
    assert cli.git_first_seen_index(nested) == {}
