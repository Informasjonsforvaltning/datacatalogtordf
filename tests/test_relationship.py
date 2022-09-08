"""Test cases for the relationship module."""
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization

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


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a title graph isomorphic to spec."""
    relationship = Relationship()
    relationship.had_role = "http://www.iana.org/assignments/relation/original"
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    relationship.relation = dataset

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
     a dcat:Relationship ;
        dct:relation   <http://example.com/datasets/1> ;
        dcat:hadRole <http://www.iana.org/assignments/relation/original>
    .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

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


def test_to_json_should_return_relationship_as_json_dict() -> None:
    """It returns a catalog json dict."""

    dataset = Dataset()
    dataset.identifier = "http://dataset-identifier"

    rel = Relationship()
    rel.identifier = "http://rel-identifier"
    rel.relation = dataset
    rel.had_role = "dataset"
    json = rel.to_json()

    assert json == {
        "_type": "Relationship",
        "had_role": "dataset",
        "identifier": "http://rel-identifier",
        "relation": {
            "_type": "Dataset",
            "access_rights_comments": [],
            "conforms_to": [],
            "distributions": [],
            "identifier": "http://dataset-identifier",
            "is_referenced_by": [],
            "landing_page": [],
            "language": [],
            "qualified_attributions": [],
            "qualified_relation": [],
            "resource_relation": [],
            "theme": [],
        },
    }


def test_from_json_should_return_relationship() -> None:
    """It returns a catalog json dict."""

    dataset = Dataset()
    dataset.identifier = "http://dataset-identifier"

    rel = Relationship()
    rel.identifier = "http://rel-identifier"
    rel.relation = dataset
    rel.had_role = "dataset"
    json = rel.to_json()

    rel_from_json = Relationship.from_json(json)

    g1 = Graph().parse(data=rel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=rel_from_json.to_rdf(), format="turtle")

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
            print(_l)
