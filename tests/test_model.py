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


def test_no_duplicate_edges_and_no_cycle_in_the_fixture(graph):
    assert graph.duplicate_registration_edges() == []
    assert graph.raw_index_cycle_core() == []
    assert graph.registration_violations()["duplicate_edges"] == []


def test_binding_neighbors_exclude_doctrine_and_raw(cfg):
    model.clear_cache()
    g = model.load(cfg)
    full = g.neighbors()
    binding = g.binding_neighbors()
    assert g.stems["Raw Index of Alpha"] in full
    assert g.stems["Vault Design"] in full
    assert g.stems["Raw Index of Alpha"] not in binding
    assert g.stems["Vault Design"] not in binding
    # Node↔Node evidence survives
    assert g.stems["Node A"] in binding[g.stems["Node B"]]


def test_cycle_core_finds_a_seeded_cycle(vault):
    alpha = vault / "library" / "Raw" / "Raw Index of Alpha.md"
    beta = vault / "library" / "Raw" / "Raw Index of Beta.md"
    beta.write_text(beta.read_text(encoding="utf-8") + "- [[Raw Index of Alpha]]\n",
                    encoding="utf-8")
    model.clear_cache()
    g = model.load(config.load(root=vault))
    assert [p.stem for p in g.raw_index_cycle_core()] == ["Raw Index of Alpha",
                                                         "Raw Index of Beta"]


def test_duplicate_edge_is_detected(vault):
    alpha = vault / "library" / "Raw" / "Raw Index of Alpha.md"
    alpha.write_text(alpha.read_text(encoding="utf-8") + "- [[Node A]]\n", encoding="utf-8")
    model.clear_cache()
    g = model.load(config.load(root=vault))
    dupes = [(r.stem, n.stem, c) for r, n, c in g.duplicate_registration_edges()]
    assert dupes == [("Raw Index of Alpha", "Node A", 2)]


def test_multi_parent_registration_is_visible(graph):
    assert graph.multi_registered() == {"Node Shared": ["Raw Index of Alpha",
                                                       "Raw Index of Beta"]}
    assert sorted(n.stem for n in graph.unregistered()) == ["Fence Node", "Node Zero"]


def test_multi_parent_is_legal_under_dag(graph):
    """DAG: uniqueness lives in the edge, so two parents are not a violation."""
    violations = graph.registration_violations()
    assert violations["multi_parent"] == {}
    assert violations["duplicate_edges"] == []
    assert graph.config.trunk_model == "dag"


def test_tree_model_still_reports_multi_parent(tmp_path, vault):
    """The trunk model is the single switch: flip it and the rule comes back."""
    text = config.CONFIG_PATH.read_text(encoding="utf-8")
    cfg_path = tmp_path / "vault.toml"
    cfg_path.write_text(text.replace('model = "dag"', 'model = "tree"'), encoding="utf-8")
    cfg = config.load(root=vault, config_path=cfg_path)
    model.clear_cache()
    g = model.load(cfg)
    assert g.config.trunk_model == "tree"
    assert g.registration_violations()["multi_parent"] == {
        "Node Shared": ["Raw Index of Alpha", "Raw Index of Beta"]}


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
    assert cfg.trunk_model == "dag"
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
