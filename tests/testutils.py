"""Utils for displaying debug information."""

from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic


def assert_isomorphic(g1: Graph, g2: Graph) -> None:
    """Compares two graphs an asserts that they are isomorphic.

        If not isomorpic a graph diff will be dumped.

    Args:
        g1 (Graph): a graph to compare
        g2 (Graph): the graph to compare with

    """
    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
    assert _isomorphic


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="turtle").splitlines():
        if _l:
            print(_l.decode())
