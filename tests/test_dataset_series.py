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


def test_to_json_should_return_dataset_series_as_json_dict() -> None:
    """It returns a catalog json dict."""
    dataset1 = Dataset()
    dataset1.identifier = "http://dataset1-identifier"
    dataset1.title = {"en": "dataset1 title"}
    dataset1.description = {"en": "dataset1 description"}
    dataset1.conforms_to = ["http://dataset1-conforms-to"]
    dataset1.keyword = {"en": "keyword"}
    dataset1.language = ["http://language"]

    dataset2 = Dataset()
    dataset2.identifier = "http://dataset2-identifier"
    dataset2.title = {"en": "dataset2 title"}
    dataset2.description = {"en": "dataset2 description"}
    dataset2.conforms_to = ["http://dataset2-conforms-to"]
    dataset2.keyword = {"en": "keyword"}
    dataset2.language = ["http://language"]
    dataset2.prev = dataset1

    dataset_series = DatasetSeries()
    dataset_series.identifier = "http://dataset_series-identifier"
    dataset_series.title = {"en": "dataset_series title"}
    dataset_series.description = {"en": "dataset_series description"}
    dataset_series.conforms_to = ["http://dataset_series-conforms-to"]
    dataset_series.keyword = {"en": "keyword"}
    dataset_series.first = dataset1
    dataset_series.last = dataset2

    json = dataset_series.to_json()

    assert json == {
        "_type": "DatasetSeries",
        "access_rights_comments": [],
        "conforms_to": ["http://dataset_series-conforms-to"],
        "description": {"en": "dataset_series description"},
        "distributions": [],
        "first": {
            "_type": "Dataset",
            "access_rights_comments": [],
            "conforms_to": ["http://dataset1-conforms-to"],
            "description": {"en": "dataset1 description"},
            "distributions": [],
            "identifier": "http://dataset1-identifier",
            "is_referenced_by": [],
            "keyword": {"en": "keyword"},
            "landing_page": [],
            "language": ["http://language"],
            "qualified_attributions": [],
            "qualified_relation": [],
            "resource_relation": [],
            "theme": [],
            "title": {"en": "dataset1 title"},
        },
        "identifier": "http://dataset_series-identifier",
        "is_referenced_by": [],
        "keyword": {"en": "keyword"},
        "landing_page": [],
        "language": [],
        "last": {
            "_type": "Dataset",
            "access_rights_comments": [],
            "conforms_to": ["http://dataset2-conforms-to"],
            "description": {"en": "dataset2 description"},
            "distributions": [],
            "identifier": "http://dataset2-identifier",
            "is_referenced_by": [],
            "keyword": {"en": "keyword"},
            "landing_page": [],
            "language": ["http://language"],
            "prev": {
                "_type": "Dataset",
                "access_rights_comments": [],
                "conforms_to": ["http://dataset1-conforms-to"],
                "description": {"en": "dataset1 description"},
                "distributions": [],
                "identifier": "http://dataset1-identifier",
                "is_referenced_by": [],
                "keyword": {"en": "keyword"},
                "landing_page": [],
                "language": ["http://language"],
                "qualified_attributions": [],
                "qualified_relation": [],
                "resource_relation": [],
                "theme": [],
                "title": {"en": "dataset1 title"},
            },
            "qualified_attributions": [],
            "qualified_relation": [],
            "resource_relation": [],
            "theme": [],
            "title": {"en": "dataset2 title"},
        },
        "qualified_attributions": [],
        "qualified_relation": [],
        "resource_relation": [],
        "theme": [],
        "title": {"en": "dataset_series title"},
    }


def test_from_json_should_return_dataset_series() -> None:
    """It returns a catalog json dict."""
    dataset1 = Dataset()
    dataset1.identifier = "http://dataset1-identifier"
    dataset1.title = {"en": "dataset1 title"}
    dataset1.description = {"en": "dataset1 description"}
    dataset1.conforms_to = ["http://dataset1-conforms-to"]
    dataset1.keyword = {"en": "keyword"}
    dataset1.language = ["http://language"]

    dataset2 = Dataset()
    dataset2.identifier = "http://dataset2-identifier"
    dataset2.title = {"en": "dataset2 title"}
    dataset2.description = {"en": "dataset2 description"}
    dataset2.conforms_to = ["http://dataset2-conforms-to"]
    dataset2.keyword = {"en": "keyword"}
    dataset2.language = ["http://language"]
    dataset2.prev = dataset1

    dataset_series = DatasetSeries()
    dataset_series.identifier = "http://dataset-series-identifier"
    dataset_series.title = {"en": "dataset-series title"}
    dataset_series.description = {"en": "dataset-series description"}
    dataset_series.first = dataset1
    dataset_series.last = dataset2
    dataset_series.is_referenced_by = [dataset1]

    json = dataset_series.to_json()

    dataset_series_from_json = DatasetSeries.from_json(json)

    g1 = Graph().parse(data=dataset_series.to_rdf(), format="turtle")
    g2 = Graph().parse(data=dataset_series_from_json.to_rdf(), format="turtle")

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
