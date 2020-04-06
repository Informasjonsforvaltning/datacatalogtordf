"""Test cases for the distribution module."""
from pytest import mark
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf import Distribution


def test_to_graph_should_return_title_as_graph() -> None:
    """It returns a title graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.title = {"nb": "API-distribusjon", "en": "API-distribution"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:title   "API-distribution"@en, "API-distribusjon"@nb
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_description() -> None:
    """It returns a description graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_release_date() -> None:
    """It returns a release date graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_modification_date() -> None:
    """It returns a modification date graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_license() -> None:
    """It returns a license graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_access_rights() -> None:
    """It returns a access rights graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_rights() -> None:
    """It returns a rights graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_has_policy() -> None:
    """It returns a has_policy graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_access_URL() -> None:
    """It returns a access URL graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_access_service() -> None:
    """It returns a access service graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_download_URL() -> None:
    """It returns a download URL graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_byte_size() -> None:
    """It returns a byte size graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_spatial_resolution() -> None:
    """It returns a spatial resolution graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_temporal_resolution() -> None:
    """It returns a temporal resolution graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_conforms_to() -> None:
    """It returns a conforms to graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_media_type() -> None:
    """It returns a media type graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_format() -> None:
    """It returns a format graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_compression_format() -> None:
    """It returns a compression format graph isomorphic to spec."""
    AssertionError()


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_packaging_format() -> None:
    """It returns a packaging format graph isomorphic to spec."""
    AssertionError()


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
