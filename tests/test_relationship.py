"""Test cases for the relationship module."""
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf import Dataset
from datacatalogtordf import Relationship

# import pytest


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns a title graph isomorphic to spec."""
    relationship = Relationship("http://example.com/relationships/1")
    relationship.had_role = "http://www.iana.org/assignments/relation/original"
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    relationship.relation = dataset

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/relationships/1> a dcat:Relationship ;
        dct:relation   <http://example.com/datasets/1> ;
        dcat:hadRole <http://www.iana.org/assignments/relation/original>
    .
    """
    g1 = Graph().parse(data=relationship.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_relation_as_graph() -> None:
    """It returns a title graph isomorphic to spec."""
    relationship = Relationship()
    relationship.identifier = "http://example.com/relationships/1"
    relationship.had_role = "http://www.iana.org/assignments/relation/original"
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    relationship.relation = dataset

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/relationships/1> a dcat:Relationship ;
        dct:relation   <http://example.com/datasets/1> ;
        dcat:hadRole <http://www.iana.org/assignments/relation/original>
    .
    """
    g1 = Graph().parse(data=relationship.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Utils for displaying debug information


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
