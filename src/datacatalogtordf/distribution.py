"""Distribution module for mapping a distribution to rdf.

This module contains methods for mapping a distribution object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-distribusjon>`__

Example:
    >>> from datacatalogtordf import Distribution
    >>>
    >>> distribution = Distribution()
    >>> distribution.identifier = "http://example.com/dataservices/1"
    >>> distribution.title = {"en": "Title of distribution"}
    >>>
    >>> bool(distribution.to_rdf())
    True
"""
from __future__ import annotations

from rdflib import Graph, Literal, Namespace, RDF, URIRef

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Distribution:
    """A class representing a dcat:Distribution.

    Ref: `dcat:Distribution <https://www.w3.org/TR/vocab-dcat-2/#Class:Distribution>`_

    Attributes:
        identifier: an URI uniquely identifying the resource
        publisher: an URI uniquely identifying the publisher of the resource
        title: a dict with title in multiple languages
    """

    _identifier: str
    _publisher: str
    _title: dict
    _type: URIRef

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = DCAT.Distribution
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)

    @property
    def identifier(self: Distribution) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Distribution, identifier: str) -> None:
        self._identifier = identifier

    @property
    def title(self: Distribution) -> dict:
        """Get/set for title."""
        return self._title

    @title.setter
    def title(self: Distribution, title: dict) -> None:
        self._title = title

    # -
    def to_rdf(self: Distribution, format: str = "turtle") -> str:
        """Maps the distribution to rdf.

        Args:
            format: a valid format. Default: turtle

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding="utf-8")

    # -
    def _to_graph(self: Distribution) -> Graph:

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if getattr(self, "title", None):
            self._title_to_graph()

        return self._g

    def _title_to_graph(self: Distribution) -> None:

        for key in self._title:
            self._g.add(
                (URIRef(self.identifier), DCT.title, Literal(self.title[key], lang=key))
            )
