"""Utils for displaying debug information."""
from typing import List, Union

from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf.skolemizer import Skolemizer

uuid = "284db4d2-80c2-11eb-82c3-83e80baa2f94"
skolemization = Skolemizer.get_baseurl() + ".well-known/skolem/" + uuid

uuid2 = "21043186-80ce-11eb-9829-cf7c8fc855ce"
skolemization2 = Skolemizer.get_baseurl() + ".well-known/skolem/" + uuid2

uuid3 = "279b7540-80ce-11eb-ba1a-7fa81b1658fe"
skolemization3 = Skolemizer.get_baseurl() + ".well-known/skolem/" + uuid3


class SkolemUtils:
    """Testutils for mocking more than one skolemization."""

    skolemization_counter: int
    skolemizations: List

    def __init__(self) -> None:
        """Constructor."""
        self.skolemization_counter = 0
        self.skolemizations = [skolemization, skolemization2, skolemization3]

    def get_skolemization(self) -> Union[str, None]:
        """Pops a skolemization from a stack of max 3 test skolemizations."""
        if self.skolemization_counter == 3:
            return None

        _skolemization = self.skolemizations[self.skolemization_counter]
        self.skolemization_counter = self.skolemization_counter + 1

        return _skolemization


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
