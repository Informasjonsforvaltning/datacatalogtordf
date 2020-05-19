"""Test cases for the catalog module."""
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf import Catalog, CatalogRecord, DataService, Dataset


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
        dct:hasPart <http://example.com/catalogs/2> ;
    .
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
