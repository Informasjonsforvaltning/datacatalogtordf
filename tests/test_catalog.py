"""Test cases for the catalog module."""
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf import Catalog, Dataset


def test_to_graph_should_return_publisher_as_graph() -> None:
    """It returns a publisher graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.publisher = "http://example.com/publisher/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dct:publisher   <http://example.com/publisher/1> ;
        .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_title_as_graph() -> None:
    """It returns a title graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    catalog.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
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
    catalog.datasets.append(dataset1)

    dataset2 = Dataset()
    dataset2.identifier = "http://example.com/datasets/2"
    catalog.datasets.append(dataset2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Catalog ;
        dcat:dataset    <http://example.com/datasets/1>,
                        <http://example.com/datasets/2>
        .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
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
