"""Test cases for the document module."""
import pytest
from rdflib import Graph

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


def test_to_graph_should_return_document_as_bnode() -> None:
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

        [ a foaf:Document;
                dct:title   "Title 1"@en, "Tittel 1"@nb ; ]
        .
        """
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
