"""Test cases for the relationship module."""
import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from datacatalogtordf import InvalidDateError, InvalidDateIntervalError, PeriodOfTime


def test_to_graph_should_return_start_date_as_graph() -> None:
    """It returns a start date graph isomorphic to spec."""
    period_of_time = PeriodOfTime()
    period_of_time.start_date = "2019-12-31"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    [] a dct:PeriodOfTime ;
        dcat:startDate "2019-12-31"^^xsd:date ;
    .
    """
    g1 = Graph().parse(data=period_of_time.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_end_date_as_graph() -> None:
    """It returns a start date graph isomorphic to spec."""
    period_of_time = PeriodOfTime()
    period_of_time.end_date = "2020-12-31"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    [] a dct:PeriodOfTime ;
        dcat:endDate "2020-12-31"^^xsd:date ;
    .
    """
    g1 = Graph().parse(data=period_of_time.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_invalid_start_date() -> None:
    """It does raise an InvalidDateError."""
    _period_of_time = PeriodOfTime()
    with pytest.raises(InvalidDateError):
        _period_of_time.start_date = "0000-99-99"


def test_invalid_end_date() -> None:
    """It does raise an InvalidDateError."""
    _period_of_time = PeriodOfTime()
    with pytest.raises(InvalidDateError):
        _period_of_time.end_date = "9999-99-99"


def test_invalid_interval_start_date() -> None:
    """It does raise an InvalidDateIntervalError."""
    _period_of_time = PeriodOfTime()
    _period_of_time.start_date = "2020-04-07"
    with pytest.raises(InvalidDateIntervalError):
        _period_of_time.end_date = "2020-04-06"


def test_invalid_interval_end_date() -> None:
    """It does raise an InvalidDateIntervalError."""
    _period_of_time = PeriodOfTime()
    _period_of_time.end_date = "2020-04-06"
    with pytest.raises(InvalidDateIntervalError):
        _period_of_time.start_date = "2020-04-07"


def test_to_json_should_return_partial_periodoftime_as_json_dict() -> None:
    """It returns a period of time json dict."""
    _period_of_time = PeriodOfTime()
    _period_of_time.start_date = "2022-01-01"
    _json = _period_of_time.to_json()

    assert _json == {
        "_type": "PeriodOfTime",
        "start_date": "2022-01-01",
    }


def test_to_json_should_return_periodoftime_as_json_dict() -> None:
    """It returns a period of time json dict."""
    _period_of_time = PeriodOfTime()
    _period_of_time.start_date = "2022-01-01"
    _period_of_time.end_date = "2023-12-31"
    _json = _period_of_time.to_json()

    assert _json == {
        "_type": "PeriodOfTime",
        "start_date": "2022-01-01",
        "end_date": "2023-12-31",
    }


def test_from_json_should_return_period_of_time_instance() -> None:
    """It returns a period of time instance."""
    _period_of_time = PeriodOfTime()
    _period_of_time.start_date = "2022-01-01"
    _period_of_time.end_date = "2023-12-31"
    _json = _period_of_time.to_json()

    _period_of_time_from_json = PeriodOfTime.from_json(_json)

    g1 = Graph().parse(data=_period_of_time.to_rdf(), format="turtle")
    g2 = Graph().parse(data=_period_of_time_from_json.to_rdf(), format="turtle")

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
