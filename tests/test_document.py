"""Test cases for the document module."""
import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff
from skolemizer.testutils import skolemization

from datacatalogtordf.document import Document
from tests.testutils import assert_isomorphic


def test_instantiate_document() -> None:
    """It does not raise an exception."""
    try:
        _ = Document()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    document = Document("http://example.com/documents/1")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf: <http://xmlns.com/foaf/0.1/> .

        <http://example.com/documents/1> a foaf:Document .
        """
    g1 = Graph().parse(data=document.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title_and_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    document = Document()
    document.identifier = "http://example.com/documents/1"
    document.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf: <http://xmlns.com/foaf/0.1/> .

        <http://example.com/documents/1> a foaf:Document;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    g1 = Graph().parse(data=document.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_document_skolemized(mocker: MockFixture) -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    document = Document()
    document.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf: <http://xmlns.com/foaf/0.1/> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a foaf:Document;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=document.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_language() -> None:
    """It returns an identifier graph isomorphic to spec."""
    document = Document()
    document.identifier = "http://example.com/documents/1"
    document.language = "http://example.com/languages/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf: <http://xmlns.com/foaf/0.1/> .

        <http://example.com/documents/1> a foaf:Document;
                dct:language "http://example.com/languages/1"^^dct:LinguisticSystem
        .
        """
    g1 = Graph().parse(data=document.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_json_should_return_document_as_json_dict() -> None:
    """It returns a catalog json dict."""

    doc = Document()
    doc.identifier = "http://doc-identifier"
    doc.title = {"en": "doc title"}
    doc.language = "http://language"
    json = doc.to_json()

    assert json == {
        "_type": "Document",
        "identifier": "http://doc-identifier",
        "language": "http://language",
        "title": {"en": "doc title"},
    }


def test_from_json_should_return_document() -> None:
    """It returns a document."""

    doc = Document()
    doc.identifier = "http://doc-identifier"
    doc.title = {"en": "doc title"}
    doc.language = "http://language"
    json = doc.to_json()

    doc_from_json = Document.from_json(json)

    g1 = Graph().parse(data=doc.to_rdf(), format="turtle")
    g2 = Graph().parse(data=doc_from_json.to_rdf(), format="turtle")

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
