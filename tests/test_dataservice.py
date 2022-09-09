"""Test cases for the dataservice module."""
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization

from datacatalogtordf import DataService, Dataset


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    dataService = DataService("http://example.com/dataservices/1")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
        .
    """
    g1 = Graph().parse(data=dataService.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a endpointURL graph isomorphic to spec."""
    dataService = DataService()

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a dcat:DataService ;
        .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=dataService.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_endpointURL_as_graph() -> None:
    """It returns a endpointURL graph isomorphic to spec."""
    dataService = DataService()
    dataService.identifier = "http://example.com/dataservices/1"
    dataService.endpointURL = "http://example.com/endpoints/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
        dcat:endpointURL   <http://example.com/endpoints/1>
        .
    """
    g1 = Graph().parse(data=dataService.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_endpointDescription_as_graph() -> None:
    """It returns a endpointDescription graph isomorphic to spec."""
    dataService = DataService()
    dataService.identifier = "http://example.com/dataservices/1"
    dataService.endpointDescription = "http://example.com/endpointdescription/1"
    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
        dcat:endpointDescription   <http://example.com/endpointdescription/1>
        .
    """
    g1 = Graph().parse(data=dataService.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_servesDataset_as_graph() -> None:
    """It returns a servesDataset graph isomorphic to spec."""
    dataService = DataService()
    dataService.identifier = "http://example.com/dataservices/1"

    dataset1 = Dataset()
    dataset1.identifier = "http://example.com/datasets/1"
    dataService.servesdatasets.append(dataset1)

    dataset2 = Dataset()
    dataset2.identifier = "http://example.com/datasets/2"
    dataService.servesdatasets.append(dataset2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
        dcat:servesDataset   <http://example.com/datasets/1>,
                             <http://example.com/datasets/2>
        .
    """
    g1 = Graph().parse(data=dataService.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_servesDataset_skolemization(
    mocker: MockFixture,
) -> None:
    """It returns a servesDataset graph isomorphic to spec."""
    dataService = DataService()
    dataService.identifier = "http://example.com/dataservices/1"

    dataset1 = Dataset()
    dataService.servesdatasets.append(dataset1)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
    dcat:servesDataset
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=dataService.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_media_type() -> None:
    """It returns a media type graph isomorphic to spec."""
    dataService = DataService()
    dataService.identifier = "http://example.com/dataservices/1"
    dataService.media_types.append(
        "https://www.iana.org/assignments/media-types/application/ld+json"
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
        dcat:mediaType \
        <https://www.iana.org/assignments/media-types/application/ld+json> ;
        .
    """
    g1 = Graph().parse(data=dataService.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_json_should_return_data_service_as_json_dict() -> None:
    """It returns a catalog json dict."""
    data_service = DataService()
    data_service.identifier = "http://data-service-identifier"
    data_service.title = {"en": "data-service title"}
    data_service.description = {"en": "data-service description"}
    data_service.conforms_to = ["http://data-service-conforms-to"]
    data_service.modification_date = "2022-01-02"
    data_service.keyword = {"en": "keyword"}
    json = data_service.to_json()

    assert json == {
        "_type": "DataService",
        "conforms_to": ["http://data-service-conforms-to"],
        "description": {"en": "data-service description"},
        "identifier": "http://data-service-identifier",
        "is_referenced_by": [],
        "keyword": {"en": "keyword"},
        "landing_page": [],
        "language": [],
        "media_types": [],
        "modification_date": "2022-01-02",
        "qualified_attributions": [],
        "qualified_relation": [],
        "resource_relation": [],
        "servesdatasets": [],
        "theme": [],
        "title": {"en": "data-service title"},
    }


def test_from_json_should_return_data_service() -> None:
    """It returns a catalog json dict."""
    dataset = Dataset()
    dataset.identifier = "http://dataset-identifier"
    dataset.title = {"en": "dataset title"}
    dataset.description = {"en": "dataset description"}
    dataset.conforms_to = ["http://dataset-conforms-to"]
    dataset.keyword = {"en": "keyword"}
    dataset.language = ["http://language"]

    data_service = DataService()
    data_service.identifier = "http://example.com/data-service/1"
    data_service.title = {"nb": "Service A", "en": "Service A"}
    data_service.description = {"nb": "Beskrivelse", "en": "Description"}
    data_service.conforms_to = ["http://comforms-to"]
    data_service.servesdatasets = [dataset]
    data_service.is_referenced_by = [dataset]

    json = data_service.to_json()

    data_service_from_json = DataService.from_json(json)

    g1 = Graph().parse(data=data_service.to_rdf(), format="turtle")
    g2 = Graph().parse(data=data_service_from_json.to_rdf(), format="turtle")

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
