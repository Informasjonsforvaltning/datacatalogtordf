"""Test cases for the dataset module."""
import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization

from datacatalogtordf import CatalogRecord, Dataset, InvalidURIError
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    catalogrecord = CatalogRecord("http://example.com/datasets/1")

    src = """
       @prefix dct: <http://purl.org/dc/terms/> .
       @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
       @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
       @prefix dcat: <http://www.w3.org/ns/dcat#> .

       <http://example.com/datasets/1> a dcat:CatalogRecord .
       """
    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/datasets/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:CatalogRecord .
    """
    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a skolemized identifier graph isomorphic to spec."""
    catalogrecord = CatalogRecord()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .


        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a dcat:CatalogRecord  .

        """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/catalogrecords/1"
    catalogrecord.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogrecords/1> a dcat:CatalogRecord ;
            dct:title   "Title 1"@en, "Tittel 1"@nb ;
    .
    """
    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_description() -> None:
    """It returns a description graph isomorphic to spec."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/catalogrecords/1"
    catalogrecord.description = {"nb": "Beskrivelse", "en": "Description"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogrecords/1> a dcat:CatalogRecord ;
        dct:description   "Description"@en, "Beskrivelse"@nb ;
        .
    """
    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_listing_date() -> None:
    """It returns a listing_date graph isomorphic to spec."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/catalogrecords/1"
    catalogrecord.listing_date = "2019-12-31"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/catalogrecords/1> a dcat:CatalogRecord ;
        dct:issued "2019-12-31"^^xsd:date ;
    .
    """
    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_modification_date() -> None:
    """It returns a modification_date graph isomorphic to spec."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/catalogrecords/1"
    catalogrecord.modification_date = "2019-12-31"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/catalogrecords/1> a dcat:CatalogRecord ;
        dct:modified "2019-12-31"^^xsd:date ;
    .
    """
    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_primary_topic() -> None:
    """It returns a primary_topic graph isomorphic to spec."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/catalogrecords/1"
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    catalogrecord.primary_topic = dataset

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .


    <http://example.com/catalogrecords/1> a dcat:CatalogRecord ;
        foaf:primaryTopic <http://example.com/datasets/1>;
    .
    """
    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_primary_topic_skolemization(
    mocker: MockFixture,
) -> None:
    """It returns a primary_topic graph isomorphic to spec."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/catalogrecords/1"
    dataset = Dataset()
    catalogrecord.primary_topic = dataset

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .


    <http://example.com/catalogrecords/1> a dcat:CatalogRecord ;
        foaf:primaryTopic
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_conforms_to() -> None:
    """It returns a conforms_to graph isomorphic to spec."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/catalogrecords/1"
    catalogrecord.conforms_to.append("http://example.com/standards/1")
    catalogrecord.conforms_to.append("http://example.com/standards/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogrecords/1> a dcat:CatalogRecord ;
        dct:conformsTo   <http://example.com/standards/1> ,
                         <http://example.com/standards/2> ;
        .
    """
    g1 = Graph().parse(data=catalogrecord.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_set_conforms_to_list_of_invalid_formats() -> None:
    """Should raise InvalidURIError."""
    catalogrecord = CatalogRecord()
    catalogrecord.identifier = "http://example.com/catalogrecords/1"
    with pytest.raises(InvalidURIError):
        catalogrecord.conforms_to = ["http://invalid^.uri.com/format"]


def test_to_json_should_return_catalog_record_as_json_dict() -> None:
    """It returns a catalog json dict."""
    record = CatalogRecord()
    record.identifier = "http://record-identifier"
    record.title = {"en": "record title"}
    record.description = {"en": "record description"}
    record.conforms_to = ["http://record-conforms-to"]
    record.listing_date = "2022-01-01"
    record.modification_date = "2022-01-02"

    json = record.to_json()

    assert json == {
        "_type": "CatalogRecord",
        "conforms_to": ["http://record-conforms-to"],
        "description": {"en": "record description"},
        "identifier": "http://record-identifier",
        "listing_date": "2022-01-01",
        "modification_date": "2022-01-02",
        "title": {"en": "record title"},
    }


def test_from_json_should_return_catalog_record() -> None:
    """It returns a catalog json dict."""
    dataset = Dataset()
    dataset.identifier = "http://dataset-identifier"
    dataset.title = {"en": "dataset title"}
    dataset.description = {"en": "dataset description"}
    dataset.conforms_to = ["http://dataset-conforms-to"]
    dataset.keyword = {"en": "keyword"}
    dataset.language = ["http://language"]

    record = CatalogRecord()
    record.identifier = "http://example.com/catalogs/1"
    record.title = {"nb": "Denne katalogen", "en": "This catalog"}
    record.description = {"nb": "Beskrivelse", "en": "Description"}
    record.conforms_to = ["http://comforms-to"]
    record.listing_date = "2022-01-01"
    record.modification_date = "2022-01-02"
    record.primary_topic = dataset

    json = record.to_json()

    catalog_record_from_json = CatalogRecord.from_json(json)

    g1 = Graph().parse(data=record.to_rdf(), format="turtle")
    g2 = Graph().parse(data=catalog_record_from_json.to_rdf(), format="turtle")

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
