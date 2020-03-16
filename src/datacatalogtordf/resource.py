"""Resource module for mapping a sub-classes to rdf.

This module contains methods for mapping a sub-class objects to rdf
according to the [dcat-ap-no v.2 standard](https://doc.difi.no/review/dcat-ap-no/)

Refer to sub-class for typical usage examples.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from rdflib import Graph, Literal, Namespace, RDF, URIRef

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Resource(ABC):
    """An abstract class representing dcat:Resource.

    Attributes:
        identifier: an URI uniquely identifying the resource
        publisher: an URI uniquely identifying the publisher of the resource
        title: a dict with title in multiple languages
    """

    _identifier: str
    _publisher: str
    _title: dict

    @abstractmethod
    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = DCAT.Resource
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)

    @property
    def identifier(self: Resource) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Resource, identifier: str) -> None:
        self._identifier = identifier

    @property
    def publisher(self: Resource) -> str:
        """Get/set for publisher."""
        return self._publisher

    @publisher.setter
    def publisher(self: Resource, publisher: str) -> None:
        self._publisher = publisher

    @property
    def title(self: Resource) -> dict:
        """Get/set for title."""
        return self._title

    @title.setter
    def title(self: Resource, title: dict) -> None:
        self._title = title

    # -
    def to_rdf(self: Resource, format: str = "turtle") -> str:
        """Maps the distribution to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format: a valid format.

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding="utf-8")

    # -
    def _to_graph(self: Resource) -> Graph:

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if getattr(self, "publisher", None):
            self._publisher_to_graph()
        if getattr(self, "title", None):
            self._title_to_graph()

        return self._g

    def _publisher_to_graph(self: Resource) -> None:

        self._g.add((URIRef(self.identifier), DCT.publisher, URIRef(self.publisher)))

    def _title_to_graph(self: Resource) -> None:

        for key in self.title:
            self._g.add(
                (URIRef(self.identifier), DCT.title, Literal(self.title[key], lang=key))
            )
