"""Test cases for the catalog module."""

from typing import Any

from pytest_mock import MockFixture
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization, SkolemUtils

from datacatalogtordf import Agent, Catalog, CatalogRecord, DataService, Dataset
from tests.testutils import assert_isomorphic

DCT = Namespace("http://purl.org/dc/terms/")
MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
CPSVNO = Namespace("https://data.norge.no/vocabulary/cpsvno#")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns a identifier graph isomorphic to spec."""
    catalog = Catalog("http://example.com/catalogs/1")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/catalogs/1> a dcat:Catalog .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_homepage() -> None:
    """It returns a homepage graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.homepage = "http://example.org/catalog"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        foaf:homepage <http://example.org/catalog> ;
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_themes() -> None:
    """It returns a themes graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.themes.append("http://example.org/sometheme")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:themeTaxonomy <http://example.org/sometheme> ;
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_part() -> None:
    """It returns a has part graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    part = Catalog()
    part.identifier = "http://example.com/catalogs/2"
    catalog.has_parts.append(part)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dct:hasPart <http://example.com/catalogs/2> .

    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_dataset_as_graph() -> None:
    """It returns a dataset graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    dataset1 = Dataset()
    dataset1.identifier = "http://example.com/datasets/1"
    dataset1.title = {"nb": "Datasett 1", "en": "Dataset 1"}
    catalog.datasets.append(dataset1)

    dataset2 = Dataset()
    dataset2.identifier = "http://example.com/datasets/2"
    dataset2.title = {"nb": "Datasett 2", "en": "Dataset 2"}
    catalog.datasets.append(dataset2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:dataset    <http://example.com/datasets/1> ,
                        <http://example.com/datasets/2> ;
    .
    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:title   "Dataset 1"@en, "Datasett 1"@nb ;
    .
    <http://example.com/datasets/2> a dcat:Dataset ;
        dct:title   "Dataset 2"@en, "Datasett 2"@nb ;
    .

    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_catalog_without_datasets_as_graph() -> None:
    """It returns a catalog graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    dataset1 = Dataset()
    dataset1.identifier = "http://example.com/datasets/1"
    dataset1.title = {"nb": "Datasett 1", "en": "Dataset 1"}
    catalog.datasets.append(dataset1)

    dataset2 = Dataset()
    dataset2.identifier = "http://example.com/datasets/2"
    dataset2.title = {"nb": "Datasett 2", "en": "Dataset 2"}
    catalog.datasets.append(dataset2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:dataset    <http://example.com/datasets/1> ,
                        <http://example.com/datasets/2> ;
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(include_datasets=False), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_service() -> None:
    """It returns a service graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    service1 = DataService()
    service1.identifier = "http://example.com/services/1"
    service1.title = {"nb": "Datatjeneste 1", "en": "Dataservice 1"}
    catalog.services.append(service1)

    service2 = DataService()
    service2.identifier = "http://example.com/services/2"
    service2.title = {"nb": "Datatjeneste 2", "en": "Dataservice 2"}
    catalog.services.append(service2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:service    <http://example.com/services/1>,
                        <http://example.com/services/2>
    .
    <http://example.com/services/1> a dcat:DataService ;
        dct:title   "Dataservice 1"@en, "Datatjeneste 1"@nb ;
    .
    <http://example.com/services/2> a dcat:DataService ;
        dct:title   "Dataservice 2"@en, "Datatjeneste 2"@nb ;
    .

    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_catalog_without_services_as_graph() -> None:
    """It returns a catalog graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    service1 = DataService()
    service1.identifier = "http://example.com/services/1"
    service1.title = {"nb": "Datatjeneste 1", "en": "Dataservice 1"}
    catalog.services.append(service1)

    service2 = DataService()
    service2.identifier = "http://example.com/services/2"
    service2.title = {"nb": "Datatjeneste 2", "en": "Dataservice 2"}
    catalog.services.append(service2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:service    <http://example.com/services/1>,
                        <http://example.com/services/2>
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(include_services=False), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_catalog() -> None:
    """It returns a catalog graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    another_catalog = Catalog()
    another_catalog.identifier = "http://example.com/catalogs/2"
    catalog.catalogs.append(another_catalog)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:catalog <http://example.com/catalogs/2> ;
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_catalog_record() -> None:
    """It returns a catalog record graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    a_catalogrecord = CatalogRecord()
    a_catalogrecord.identifier = "http://example.com/catalogrecords/1"
    catalog.catalogrecords.append(a_catalogrecord)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:record <http://example.com/catalogrecords/1> ;
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_catalog_without_removed_service_as_graph() -> None:
    """It returns a catalog graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    service1 = DataService()
    service1.identifier = "http://example.com/services/1"
    service1.title = {"nb": "Datatjeneste 1", "en": "Dataservice 1"}
    catalog.services.append(service1)

    service2 = DataService()
    service2.identifier = "http://example.com/services/2"
    service2.title = {"nb": "Datatjeneste 2", "en": "Dataservice 2"}
    catalog.services.append(service2)

    # Generate graph
    _ = Graph().parse(data=catalog.to_rdf(include_services=False), format="turtle")

    # Remove second item
    del catalog.services[1]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:service    <http://example.com/services/1>
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(include_services=False), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _dump_turtle(g1)
    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def model_to_graph(model: Any) -> Graph:
    """Helper function to create a model graph to test with."""
    g = Graph()

    g.add((URIRef(model.identifier), RDF.type, MODELLDCATNO.InformationModel))

    for key in model.title:
        g.add(
            (
                URIRef(model.identifier),
                DCT.title,
                Literal(model.title[key], lang=key),
            )
        )

    return g


def test_to_graph_should_return_dct_identifier_as_graph() -> None:
    """It returns a dct_identifier graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.dct_identifier = "Catalog_123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1>    a dcat:Catalog ;
        dct:identifier "Catalog_123456789";
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_blank_skolemization(mocker: MockFixture) -> None:
    """It returns a catalog graph as blank node isomorphic to spec."""
    catalog = Catalog()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a dcat:Catalog  .

        """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_part_skolemization(mocker: MockFixture) -> None:
    """It returns a has has_part graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    part = Catalog()
    catalog.has_parts.append(part)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dct:hasPart
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> .

    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_dataset_skolemization(mocker: MockFixture) -> None:
    """It returns a dataset graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    dataset1 = Dataset()
    dataset1.title = {"nb": "Datasett 1", "en": "Dataset 1"}
    catalog.datasets.append(dataset1)

    dataset2 = Dataset()
    dataset2.title = {"nb": "Datasett 2", "en": "Dataset 2"}
    catalog.datasets.append(dataset2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:dataset
            <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce> ,
            <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> ;
    .
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
     a dcat:Dataset ;
        dct:title   "Dataset 1"@en, "Datasett 1"@nb ;
    .
    <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
     a dcat:Dataset ;
        dct:title   "Dataset 2"@en, "Datasett 2"@nb ;
    .

    """

    skolemutils = SkolemUtils()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_dataservice_skolemization(mocker: MockFixture) -> None:
    """It returns a dataservice graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    dataservice1 = DataService()
    dataservice1.title = {"nb": "Dataservice 1", "en": "Dataservice 1"}
    catalog.services.append(dataservice1)

    dataservice2 = DataService()
    dataservice2.title = {"nb": "Dataservice 2", "en": "Dataservice 2"}
    catalog.services.append(dataservice2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:service
            <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce> ,
            <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> ;
    .
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
     a dcat:DataService ;
        dct:title   "Dataservice 1"@en, "Dataservice 1"@nb ;
    .
    <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
     a dcat:DataService ;
        dct:title   "Dataservice 2"@en, "Dataservice 2"@nb ;
    .

    """

    skolemutils = SkolemUtils()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_catalog_skolemization(mocker: MockFixture) -> None:
    """It returns a has catalog graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    part = Catalog()
    catalog.catalogs.append(part)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:catalog
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> .

    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_catalog_record_skolemization(
    mocker: MockFixture,
) -> None:
    """It returns a catalog record graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    a_catalogrecord = CatalogRecord()

    catalog.catalogrecords.append(a_catalogrecord)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:record
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_json_should_return_partial_catalog_as_json_dict() -> None:
    """It returns a catalog json dict."""
    publisher = Agent()
    publisher.identifier = "http://publisher"

    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.publisher = publisher
    json = catalog.to_json()

    assert json == {
        "_type": "Catalog",
        "access_rights_comments": [],
        "catalogrecords": [],
        "catalogs": [],
        "conforms_to": [],
        "datasets": [],
        "distributions": [],
        "has_parts": [],
        "identifier": "http://example.com/catalogs/1",
        "is_referenced_by": [],
        "landing_page": [],
        "language": [],
        "publisher": {"_type": "Agent", "identifier": "http://publisher"},
        "qualified_attributions": [],
        "qualified_relation": [],
        "resource_relation": [],
        "services": [],
        "theme": [],
        "themes": [],
    }


def test_to_json_should_return_catalog_as_json_dict() -> None:
    """It returns a catalog json dict."""
    other_catalog1 = Catalog()
    other_catalog1.identifier = "http://example.com/catalog/other1"

    other_catalog2 = Catalog()
    other_catalog2.identifier = "http://example.com/catalog/other2"

    catalog_record = CatalogRecord()
    catalog_record.identifier = "http://example.com/catalog-record/1"

    data_service = DataService()
    data_service.identifier = "http://example.com/data-service/1"

    dataset1 = Dataset()
    dataset1.identifier = "http://example.com/datasets/1"
    dataset1.title = {"nb": "Datasett 1", "en": "Dataset 1"}
    dataset1.frequency = "http://WEEKLY"

    dataset2 = Dataset()
    dataset2.identifier = "http://example.com/datasets/2"
    dataset2.title = {"nb": "Datasett 2", "en": "Dataset 2"}

    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.title = {"nb": "Denne katalogen", "en": "This catalog"}
    catalog.description = {"nb": "Beskrivelse", "en": "Description"}
    catalog.has_parts.append(other_catalog2)
    catalog.catalogs.append(other_catalog1)
    catalog.catalogrecords.append(catalog_record)
    catalog.datasets.append(dataset1)
    catalog.datasets.append(dataset2)
    catalog.services.append(data_service)

    json = catalog.to_json()

    assert json == {
        "_type": "Catalog",
        "access_rights_comments": [],
        "catalogrecords": [
            {
                "_type": "CatalogRecord",
                "conforms_to": [],
                "identifier": "http://example.com/catalog-record/1",
            }
        ],
        "catalogs": [
            {
                "_type": "Catalog",
                "access_rights_comments": [],
                "catalogrecords": [],
                "catalogs": [],
                "conforms_to": [],
                "datasets": [],
                "distributions": [],
                "has_parts": [],
                "identifier": "http://example.com/catalog/other1",
                "is_referenced_by": [],
                "landing_page": [],
                "language": [],
                "qualified_attributions": [],
                "qualified_relation": [],
                "resource_relation": [],
                "services": [],
                "theme": [],
                "themes": [],
            }
        ],
        "conforms_to": [],
        "datasets": [
            {
                "_type": "Dataset",
                "access_rights_comments": [],
                "conforms_to": [],
                "distributions": [],
                "frequency": "http://WEEKLY",
                "identifier": "http://example.com/datasets/1",
                "is_referenced_by": [],
                "landing_page": [],
                "language": [],
                "qualified_attributions": [],
                "qualified_relation": [],
                "resource_relation": [],
                "theme": [],
                "title": {"en": "Dataset 1", "nb": "Datasett 1"},
            },
            {
                "_type": "Dataset",
                "access_rights_comments": [],
                "conforms_to": [],
                "distributions": [],
                "identifier": "http://example.com/datasets/2",
                "is_referenced_by": [],
                "landing_page": [],
                "language": [],
                "qualified_attributions": [],
                "qualified_relation": [],
                "resource_relation": [],
                "theme": [],
                "title": {"en": "Dataset 2", "nb": "Datasett 2"},
            },
        ],
        "description": {"en": "Description", "nb": "Beskrivelse"},
        "distributions": [],
        "has_parts": [
            {
                "_type": "Catalog",
                "access_rights_comments": [],
                "catalogrecords": [],
                "catalogs": [],
                "conforms_to": [],
                "datasets": [],
                "distributions": [],
                "has_parts": [],
                "identifier": "http://example.com/catalog/other2",
                "is_referenced_by": [],
                "landing_page": [],
                "language": [],
                "qualified_attributions": [],
                "qualified_relation": [],
                "resource_relation": [],
                "services": [],
                "theme": [],
                "themes": [],
            }
        ],
        "identifier": "http://example.com/catalogs/1",
        "is_referenced_by": [],
        "landing_page": [],
        "language": [],
        "qualified_attributions": [],
        "qualified_relation": [],
        "resource_relation": [],
        "services": [
            {
                "_type": "DataService",
                "conforms_to": [],
                "identifier": "http://example.com/data-service/1",
                "is_referenced_by": [],
                "landing_page": [],
                "language": [],
                "media_types": [],
                "qualified_attributions": [],
                "qualified_relation": [],
                "resource_relation": [],
                "servesdatasets": [],
                "theme": [],
            }
        ],
        "theme": [],
        "themes": [],
        "title": {"en": "This catalog", "nb": "Denne katalogen"},
    }


def test_from_json_should_return_catalog() -> None:
    """It returns a catalog json dict."""
    other_catalog1 = Catalog()
    other_catalog1.identifier = "http://example.com/catalog/other1"

    other_catalog2 = Catalog()
    other_catalog2.identifier = "http://example.com/catalog/other2"

    catalog_record = CatalogRecord()
    catalog_record.identifier = "http://example.com/catalog-record/1"

    data_service = DataService()
    data_service.identifier = "http://example.com/data-service/1"

    dataset1 = Dataset()
    dataset1.identifier = "http://example.com/datasets/1"
    dataset1.title = {"nb": "Datasett 1", "en": "Dataset 1"}
    dataset1.frequency = "http://WEEKLY"

    dataset2 = Dataset()
    dataset2.identifier = "http://example.com/datasets/2"
    dataset2.title = {"nb": "Datasett 2", "en": "Dataset 2"}

    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.title = {"nb": "Denne katalogen", "en": "This catalog"}
    catalog.description = {"nb": "Beskrivelse", "en": "Description"}
    catalog.has_parts.append(other_catalog2)
    catalog.catalogs.append(other_catalog1)
    catalog.catalogrecords.append(catalog_record)
    catalog.datasets.append(dataset1)
    catalog.datasets.append(dataset2)
    catalog.services.append(data_service)
    catalog.is_referenced_by = [other_catalog2]

    json = catalog.to_json()

    catalog_from_json = Catalog.from_json(json)

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=catalog_from_json.to_rdf(), format="turtle")

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
