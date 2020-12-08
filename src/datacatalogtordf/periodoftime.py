"""PeriodOfTime module for mapping a period_of_time to rdf.

This module contains methods for mapping a period_of_time object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-distribusjon>`__

Example:
    >>> from datacatalogtordf import PeriodOfTime
    >>>
    >>> period_of_time = PeriodOfTime()
    >>> period_of_time.start_date = "2019-12-31"
    >>> period_of_time.end_date = "2020-12-31"
    >>>
    >>> bool(period_of_time.to_rdf())
    True
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

from .exceptions import InvalidDateError, InvalidDateIntervalError


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


class Date(str):
    """A helper class to validate a Date.

    If the string is a valid of the format "%Y-%m-%d",
    it is valid. Otherwise not.

    Raises:
        InvalidDateError: If the str does not represent a valid date
    """

    def __init__(self, link: str) -> None:
        """Validate a Date object."""
        try:
            self._is_valid_date(link)
        except Exception as err:
            raise InvalidDateError(link, str(err))

    # -
    def _is_valid_date(self: Date, date: str) -> None:
        """Perform basic validation of str as date."""
        try:
            _ = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise InvalidDateError(date, "String is not a valid date")


class PeriodOfTime:
    """A class representing a dcat:PeriodOfTime.

    Ref: `dcat:PeriodOfTime <https://www.w3.org/TR/vocab-dcat-2/#Class:PeriodOfTime>`_

    Attributes:
        start_date: date signfying the start of the period
        end_date: date signfying the end of the period

    Raises:
        InvalidDateIntervalError: If the interval is "negative", i.e. \
            start date is after the end date
    """

    slots = ("_identifier", "_start_date", "_end_date")

    _start_date: str
    _end_date: str
    _ref: URIRef

    def __init__(self) -> None:
        """Inits an object with default values."""
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("xsd", XSD)

    @property
    def start_date(self: PeriodOfTime) -> str:
        """Get/set for start_date."""
        return self._start_date

    @start_date.setter
    def start_date(self: PeriodOfTime, start_date: str) -> None:
        _date = Date(start_date)
        # Check for invalid interval:
        if getattr(self, "end_date", None):
            if not self._is_valid_interval(start_date, self.end_date):
                raise InvalidDateIntervalError(
                    start_date, self.end_date, "start_date after end_date"
                )
        self._start_date = _date

    @property
    def end_date(self: PeriodOfTime) -> str:
        """Get/set for end_date."""
        return self._end_date

    @end_date.setter
    def end_date(self: PeriodOfTime, end_date: str) -> None:
        _date = Date(end_date)
        # Check for invalid interval:
        if getattr(self, "start_date", None):
            if not self._is_valid_interval(self.start_date, end_date):
                raise InvalidDateIntervalError(
                    end_date, self.start_date, "start_date after end_date"
                )
        self._end_date = _date

    # -
    def to_rdf(
        self: PeriodOfTime, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the period_of_time to rdf."""
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -
    def _to_graph(self: PeriodOfTime) -> Graph:

        self._ref = BNode()
        self._g.add((self._ref, RDF.type, DCT.PeriodOfTime))

        self._start_date_to_graph()
        self._end_date_to_graph()

        return self._g

    # -
    def _start_date_to_graph(self: PeriodOfTime) -> None:
        if getattr(self, "start_date", None):
            self._g.add(
                (
                    self._ref,
                    DCAT.startDate,
                    Literal(self.start_date, datatype=XSD.date),
                )
            )

    def _end_date_to_graph(self: PeriodOfTime) -> None:
        if getattr(self, "end_date", None):
            self._g.add(
                (
                    self._ref,
                    DCAT.endDate,
                    Literal(self.end_date, datatype=XSD.date),
                )
            )

    # - helpers
    def _is_valid_interval(self: PeriodOfTime, start_date: str, end_date: str) -> bool:
        if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(
            end_date, "%Y-%m-%d"
        ):
            return False
        return True
