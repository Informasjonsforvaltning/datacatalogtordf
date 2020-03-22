"""Test cases for the resource module."""
import pytest
from pytest import mark
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf import Dataset, Resource

"""
A test class for testing the _abstract_ class Resource.
Using Dataset class in order to instantiate Resource.
"""


def test_instantiate_resource_should_fail_with_TypeError() -> None:
    """It returns a TypeErro exception."""
    with pytest.raises(TypeError):
        _ = Resource()  # type: ignore


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_publisher() -> None:
    """It returns a publisher graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"
    resource.publisher = "http://example.com/publisher/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:publisher   <http://example.com/publisher/1> ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_title() -> None:
    """It returns a title graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"
    resource.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_accessRights() -> None:
    """It returns a accessRights graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"
    accessRights = "PUBLIC"
    resource.accessRights = (
        f"http://publications.europa.eu/resource/authority/access-right/{accessRights}"
    )

    src = (
        "@prefix dct: <http://purl.org/dc/terms/> ."
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ."
        "@prefix dcat: <http://www.w3.org/ns/dcat#> .\n"
        "<http://example.com/datasets/1> a dcat:Dataset ;"
        "\tdct:accessRights\t"
        "<http://publications.europa.eu/resource/authority/access-right/"
        f"{accessRights}> ."
    )
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_conformsTo() -> None:
    """It returns a conformsTo graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"
    resource.conformsTo.append("http://example.com/standards/1")
    resource.conformsTo.append("http://example.com/standards/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:conformsTo   <http://example.com/standards/1> ,
                         <http://example.com/standards/2> ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_contactPoint() -> None:
    """It returns a contactPoint graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_creator() -> None:
    """It returns a creator graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_description() -> None:
    """It returns a description graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"
    resource.description = {"nb": "Beskrivelse", "en": "Description"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:description   "Description"@en, "Beskrivelse"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_hasPolicy() -> None:
    """It returns a hasPolicy graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_isReferencedBy() -> None:
    """It returns a accessRights isReferencedBy isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_keyword() -> None:
    """It returns a keyword graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_landingPage() -> None:
    """It returns a landingPage graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_license() -> None:
    """It returns a license graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_language() -> None:
    """It returns a language graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_relation() -> None:
    """It returns a relation graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_rights() -> None:
    """It returns a rights graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_qualifiedRelation() -> None:
    """It returns a qualifiedRelation graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_releaseDate() -> None:
    """It returns a releaseDate graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_theme() -> None:
    """It returns a theme graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"
    resource.theme.append("http://example.com/themes/1")
    resource.theme.append("http://example.com/themes/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dcat:theme   <http://example.com/themes/1> ,
                     <http://example.com/themes/2> ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_type() -> None:
    """It returns a type graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_modificationDate() -> None:
    """It returns a modificationDate graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=True, reason="Not implemented")
def test_to_graph_should_return_qualifiedAttribution() -> None:
    """It returns a qualifiedAttribution graph isomorphic to spec."""
    resource = Dataset()
    resource.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    """
    g1 = Graph().parse(data=resource.to_rdf(), format="turtle")
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
    for l in g.serialize(format="turtle").splitlines():
        if l:
            print(l.decode())
