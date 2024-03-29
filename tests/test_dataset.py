"""Test cases for the dataset module."""
from decimal import Decimal

import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization

from datacatalogtordf import (
    Agent,
    Contact,
    Dataset,
    DatasetSeries,
    Distribution,
    InvalidURIError,
    Location,
    PeriodOfTime,
    Relationship,
)


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns a identifier graph isomorphic to spec."""
    dataset = Dataset("http://example.com/datasets/1")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/datasets/1> a dcat:Dataset .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a endpointURL graph isomorphic to spec."""
    dataset = Dataset()

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a dcat:Dataset ;
        .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_distribution_as_graph() -> None:
    """It returns a distribution graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"

    distribution1 = Distribution()
    distribution1.identifier = "http://example.com/distributions/1"
    dataset.distributions.append(distribution1)

    distribution2 = Distribution()
    distribution2.identifier = "http://example.com/distributions/2"
    dataset.distributions.append(distribution2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix prov: <http://www.w3.org/ns/prov#> .


    <http://example.com/datasets/1> a dcat:Dataset ;
        dcat:distribution   <http://example.com/distributions/1>,
                            <http://example.com/distributions/2>
        .
    """
    g1 = Graph().parse(
        data=dataset.to_rdf(include_distributions=False), format="turtle"
    )
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_distribution_skolemized(mocker: MockFixture) -> None:
    """It returns a distribution graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"

    distribution1 = Distribution()
    dataset.distributions.append(distribution1)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix prov: <http://www.w3.org/ns/prov#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dcat:distribution
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(
        data=dataset.to_rdf(include_distributions=False), format="turtle"
    )
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_included_distribution_as_graph() -> None:
    """It returns a dataset graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"

    distribution1 = Distribution()
    distribution1.identifier = "http://example.com/distributions/1"
    distribution1.title = {"nb": "API-distribusjon 1", "en": "API-distribution 1"}

    dataset.distributions.append(distribution1)

    distribution2 = Distribution()
    distribution2.identifier = "http://example.com/distributions/2"
    distribution2.title = {"nb": "API-distribusjon 2", "en": "API-distribution 2"}
    dataset.distributions.append(distribution2)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix prov: <http://www.w3.org/ns/prov#> .


    <http://example.com/datasets/1> a dcat:Dataset ;
        dcat:distribution   <http://example.com/distributions/1>,
                            <http://example.com/distributions/2>
    .
    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:title   "API-distribution 1"@en, "API-distribusjon 1"@nb ;
    .
    <http://example.com/distributions/2> a dcat:Distribution ;
        dct:title   "API-distribution 2"@en, "API-distribusjon 2"@nb ;
    .

    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_frequency() -> None:
    """It returns a frequency graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    dataset.frequency = "http://purl.org/cld/freq/daily"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:accrualPeriodicity   <http://purl.org/cld/freq/daily> ;
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_spatial() -> None:
    """It returns a spatial coverage graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    # Create location:
    location = Location()
    location.centroid = "POINT(4.88412 52.37509)"
    # Add location to dataset:
    dataset.spatial = [location]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:spatial [
            a dct:Location ;
            dcat:centroid "POINT(4.88412 52.37509)"^^geosparql:asWKT ;
        ]
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_spatial_resolution_in_meters() -> None:
    """It returns a spatial resolution graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    # spatial resolution is an xsd:decimal:
    dataset.spatial_resolution_in_meters = [Decimal(30.0)]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dcat:spatialResolutionInMeters  "30.0"^^xsd:decimal
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_temporal() -> None:
    """It returns a temporal coverage graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    # Create PeriodOfTime:
    temporal = PeriodOfTime()
    temporal.start_date = "2019-12-31"
    temporal.end_date = "2020-12-31"
    # Add temporal to dataset:
    dataset.temporal = [temporal]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:temporal [ a dct:PeriodOfTime ;
            dcat:startDate "2019-12-31"^^xsd:date ;
            dcat:endDate   "2020-12-31"^^xsd:date ;
        ]
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_temporal_resolution() -> None:
    """It returns a temporal resolution graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    dataset.temporal_resolution = ["PT15M"]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
            dcat:temporalResolution "PT15M"^^xsd:duration ;
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_was_generated_by() -> None:
    """It returns a was generated by graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    dataset.was_generated_by = "http://example.com/activity/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
    @prefix prov: <http://www.w3.org/ns/prov#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
            prov:wasGeneratedBy <http://example.com/activity/1> ;
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_access_rights_comment() -> None:
    """It returns a access rights comment graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    dataset.access_rights_comments.append("http://example.com/concepts/1")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
    @prefix dcatno: <https://data.norge.no/vocabulary/dcatno#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
            dcatno:accessRightsComment <http://example.com/concepts/1> ;
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_set_access_rights_with_list_of_invalid_uris() -> None:
    """Should raise InvalidURIError."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"

    with pytest.raises(InvalidURIError):
        dataset.access_rights_comments = ["http://invalid^.uri.com/format"]


def test_to_graph_should_return_link_to_spatial() -> None:
    """It returns a spatial coverage graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    # Add link to location:
    location = "http://publications.europa.eu/resource/authority/country/NOR"
    dataset.spatial = [location]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:spatial <http://publications.europa.eu/resource/authority/country/NOR> ;
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_link_to_spatial_with_location_triple() -> None:
    """It returns a spatial coverage graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    # Create location:
    location = Location()
    location.identifier = "http://example.com/locations/1"
    location.centroid = "POINT(4.88412 52.37509)"
    # Add location to dataset:
    dataset.spatial = [location]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dct:spatial <http://example.com/locations/1> ;
    .

    <http://example.com/locations/1> a dct:Location ;
            dcat:centroid "POINT(4.88412 52.37509)"^^geosparql:asWKT ;
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_dct_identifier_as_graph() -> None:
    """It returns a dct_identifier graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    dataset.dct_identifier = "Dataset_123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1>    a dcat:Dataset ;
        dct:identifier "Dataset_123456789";
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_json_should_return_dataset_as_json_dict() -> None:
    """It returns a catalog json dict."""
    dataset = Dataset()
    dataset.identifier = "http://dataset-identifier"
    dataset.title = {"en": "dataset title"}
    dataset.description = {"en": "dataset description"}
    dataset.conforms_to = ["http://dataset-conforms-to"]
    dataset.keyword = {"en": "keyword"}
    dataset.language = ["http://language"]

    dist = Distribution()
    dist.identifier = "http://distribution-identifier"
    dist.title = {"en": "dist title"}
    dist.description = {"en": "dist description"}
    dist.formats = ["http://csv", "http://xml"]
    dist.license = "http://license"
    dataset.distributions = [dist]

    json = dataset.to_json()

    assert json == {
        "_type": "Dataset",
        "access_rights_comments": [],
        "conforms_to": ["http://dataset-conforms-to"],
        "description": {"en": "dataset description"},
        "distributions": [
            {
                "_type": "Distribution",
                "conforms_to": [],
                "description": {"en": "dist description"},
                "formats": ["http://csv", "http://xml"],
                "identifier": "http://distribution-identifier",
                "license": "http://license",
                "media_types": [],
                "title": {"en": "dist title"},
            }
        ],
        "identifier": "http://dataset-identifier",
        "is_referenced_by": [],
        "keyword": {"en": "keyword"},
        "landing_page": [],
        "language": ["http://language"],
        "qualified_attributions": [],
        "qualified_relation": [],
        "resource_relation": [],
        "theme": [],
        "title": {"en": "dataset title"},
    }


def test_from_json_should_return_dataset() -> None:
    """It returns a catalog json dict."""
    agent = Agent()
    agent.identifier = "http://agent/1"

    distribution = Distribution()
    distribution.identifier = "http://example.com/data-service/1"
    distribution.title = {"nb": "Service A", "en": "Service A"}
    distribution.description = {"nb": "Beskrivelse", "en": "Description"}

    location = Location()
    location.identifier = "http://location/1"

    temporal = PeriodOfTime()
    temporal.start_date = "2022-01-01"

    series = DatasetSeries()
    series.identifier = "http://dataset-series/1"

    contact = Contact()
    contact.identifier = "http://contact/1"

    relationship = Relationship()
    relationship.identifier = "http://relationship/1"

    dataset = Dataset()
    dataset.identifier = "http://dataset-identifier"
    dataset.title = {"en": "dataset title"}
    dataset.description = {"en": "dataset description"}
    dataset.conforms_to = ["http://dataset-conforms-to"]
    dataset.keyword = {"en": "keyword"}
    dataset.language = ["http://language"]
    dataset.spatial = [location]
    dataset.temporal = [temporal]
    dataset.in_series = series
    dataset.distributions = [distribution]
    dataset.contactpoint = contact
    dataset.publisher = agent
    dataset.qualified_relation = [relationship]

    json = dataset.to_json()

    dataset_from_json = Dataset.from_json(json)

    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=dataset_from_json.to_rdf(), format="turtle")

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
