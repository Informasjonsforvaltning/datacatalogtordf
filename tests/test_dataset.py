"""Test cases for the dataset module."""
from decimal import Decimal

from pytest import mark
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf import Dataset, Distribution, Location, PeriodOfTime


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


def test_to_graph_should_return_spatial_coverage() -> None:
    """It returns a spatial coverage graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    # Create location:
    location = Location()
    location.centroid = "POINT(4.88412 52.37509)"
    # Add location to dataset:
    dataset.spatial_coverage = location

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


def test_to_graph_should_return_spatial_resolution() -> None:
    """It returns a spatial resolution graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    # spatial resolution is an xsd:decimal:
    dataset.spatial_resolution = Decimal(30.0)

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


def test_to_graph_should_return_temporal_coverage() -> None:
    """It returns a temporal coverage graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    # Create PeriodOfTime:
    period_of_time = PeriodOfTime()
    period_of_time.start_date = "2019-12-31"
    period_of_time.end_date = "2020-12-31"
    # Add period_of_time to dataset:
    dataset.period_of_time = period_of_time

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
    dataset.temporal_resolution = "PT15M"

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


@mark.xfail(strict=False, reason="Not implemented")
def test_to_graph_should_return_accessRightsComment() -> None:
    """It returns a accessRights comment graph isomorphic to spec."""
    # TODO: add support for dcatno:accessRightsComment
    AssertionError()


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
