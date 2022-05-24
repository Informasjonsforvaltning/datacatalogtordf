"""Test cases for the dataset_series module."""
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf import Catalog, Dataset, DatasetSeries


def test_catalog_to_graph_should_return_dataset_series() -> None:
    """It returns a has part graph isomorphic to spec."""
    dataset_series = DatasetSeries("http://example.org/budget")
    dataset_series.title = {"en": "Budget data"}

    catalog = Catalog("http://example.org/EUCatalog")
    catalog.title = {"en": "European Data Catalog"}
    catalog.datasets.append(dataset_series)

    first_dataset = Dataset("http://example.org/budget-2018")
    first_dataset.title = {"en": "Budget data for year 2018"}
    first_dataset.release_date = "2019-01-01"
    first_dataset.in_series = dataset_series

    second_dataset = Dataset("http://example.org/budget-2019")
    second_dataset.title = {"en": "Budget data for year 2019"}
    second_dataset.release_date = "2020-01-01"
    second_dataset.in_series = dataset_series
    second_dataset.prev = first_dataset

    third_dataset = Dataset("http://example.org/budget-2020")
    third_dataset.title = {"en": "Budget data for year 2020"}
    third_dataset.release_date = "2021-01-01"
    third_dataset.in_series = dataset_series
    third_dataset.prev = second_dataset

    dataset_series.first = first_dataset
    dataset_series.last = third_dataset

    src = """
    @prefix ex: <http://example.org/> .
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .


    ex:EUCatalog a dcat:Catalog ;
        dct:title "European Data Catalog"@en ;
        dcat:dataset ex:budget  ;
        .

    ex:budget a dcat:DatasetSeries ;
        dct:title "Budget data"@en ;
        dcat:first ex:budget-2018 ;
        dcat:last ex:budget-2020 ;
        .

    ex:budget-2018 a dcat:Dataset ;
        dct:title "Budget data for year 2018"@en ;
        dcat:inSeries ex:budget ;
        dct:issued "2019-01-01"^^xsd:date ;
        .

    ex:budget-2019 a dcat:Dataset ;
        dct:title "Budget data for year 2019"@en ;
        dcat:inSeries ex:budget ;
        dct:issued "2020-01-01"^^xsd:date ;
        dcat:prev ex:budget-2018 ;
        .

    ex:budget-2020 a dcat:Dataset ;
        dct:title "Budget data for year 2020"@en ;
        dcat:inSeries ex:budget ;
        dct:issued "2021-01-01"^^xsd:date ;
        dcat:prev ex:budget-2019 ;
        .
    """

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_dataset_series() -> None:
    """It returns a has part graph isomorphic to spec."""
    dataset_series = DatasetSeries("http://example.org/budget")
    dataset_series.title = {"en": "Budget data"}

    first_dataset = Dataset("http://example.org/budget-2018")
    first_dataset.title = {"en": "Budget data for year 2018"}
    first_dataset.release_date = "2019-01-01"
    first_dataset.in_series = dataset_series

    second_dataset = Dataset("http://example.org/budget-2019")
    second_dataset.title = {"en": "Budget data for year 2019"}
    second_dataset.release_date = "2020-01-01"
    second_dataset.in_series = dataset_series
    second_dataset.prev = first_dataset

    third_dataset = Dataset("http://example.org/budget-2020")
    third_dataset.title = {"en": "Budget data for year 2020"}
    third_dataset.release_date = "2021-01-01"
    third_dataset.in_series = dataset_series
    third_dataset.prev = second_dataset

    dataset_series.first = first_dataset
    dataset_series.last = third_dataset

    src = """
    @prefix ex: <http://example.org/> .
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .


    ex:budget a dcat:DatasetSeries ;
        dct:title "Budget data"@en ;
        dcat:first ex:budget-2018 ;
        dcat:last ex:budget-2020 ;
        .

    ex:budget-2018 a dcat:Dataset ;
        dct:title "Budget data for year 2018"@en ;
        dcat:inSeries ex:budget ;
        dct:issued "2019-01-01"^^xsd:date ;
        .

    ex:budget-2019 a dcat:Dataset ;
        dct:title "Budget data for year 2019"@en ;
        dcat:inSeries ex:budget ;
        dct:issued "2020-01-01"^^xsd:date ;
        dcat:prev ex:budget-2018 ;
        .

    ex:budget-2020 a dcat:Dataset ;
        dct:title "Budget data for year 2020"@en ;
        dcat:inSeries ex:budget ;
        dct:issued "2021-01-01"^^xsd:date ;
        dcat:prev ex:budget-2019 ;
        .
    """

    g1 = Graph().parse(data=dataset_series.to_rdf(), format="turtle")
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
            print(_l)
