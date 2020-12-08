"""Location module for mapping a location to rdf.

This module contains methods for mapping a location object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-distribusjon>`__

Example:
    >>> from datacatalogtordf import Location
    >>>
    >>> location = Location()
    >>> location.identifier = "http://example.com/relations/1"
    >>> location.centroid = "POINT(4.88412 52.37509)"
    >>>
    >>> bool(location.to_rdf())
    True
"""
from __future__ import annotations

from typing import Optional

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

from .uri import URI


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
LOCN = Namespace("http://www.w3.org/ns/locn#")
GEOSPARQL = Namespace("http://www.opengis.net/ont/geosparql#")


class Location:
    """A class representing a dcat:Location.

    Ref: `dcat:Location <https://www.w3.org/TR/vocab-dcat-2/#Class:Location>`_

    Attributes:
        identifier (URI): an URI uniquely identifying the resource
        geometry (str): Associates any resource with the corresponding geometry.
        bounding_box (str): The geographic bounding box of a resource.
        centroid (str): The geographic center (centroid) of a resource.
    """

    slots = ("_identifier", "_geometry", "_bounding_box", "_centroid")

    _identifier: URI
    _geometry: str
    _bounding_box: str
    _centroid: str
    _ref: URIRef

    def __init__(self) -> None:
        """Inits an object with default values."""
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("locn", LOCN)
        self._g.bind("geosparql", GEOSPARQL)

    @property
    def identifier(self: Location) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Location, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def geometry(self: Location) -> str:
        """Get/set for geometry."""
        return self._geometry

    @geometry.setter
    def geometry(self: Location, geometry: str) -> None:
        self._geometry = geometry

    @property
    def bounding_box(self: Location) -> str:
        """Get/set for bounding_box."""
        return self._bounding_box

    @bounding_box.setter
    def bounding_box(self: Location, bounding_box: str) -> None:
        self._bounding_box = bounding_box

    @property
    def centroid(self: Location) -> str:
        """Get/set for centroid."""
        return self._centroid

    @centroid.setter
    def centroid(self: Location, centroid: str) -> None:
        self._centroid = centroid

    # -
    def to_rdf(
        self: Location, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the location to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -
    def _to_graph(self: Location) -> Graph:

        if getattr(self, "identifier", None):
            self._ref = URIRef(self.identifier)
        else:
            self._ref = BNode()
        self._g.add((self._ref, RDF.type, DCT.Location))

        self._geometry_to_graph()
        self._bounding_box_to_graph()
        self._centroid_to_graph()

        return self._g

    # -
    def _geometry_to_graph(self: Location) -> None:
        if getattr(self, "geometry", None):
            self._g.add(
                (
                    self._ref,
                    LOCN.geometry,
                    Literal(self.geometry, datatype=GEOSPARQL.asWKT),
                )
            )

    def _bounding_box_to_graph(self: Location) -> None:
        if getattr(self, "bounding_box", None):
            self._g.add(
                (
                    self._ref,
                    DCAT.bbox,
                    Literal(self.bounding_box, datatype=GEOSPARQL.asWKT),
                )
            )

    def _centroid_to_graph(self: Location) -> None:
        if getattr(self, "centroid", None):
            self._g.add(
                (
                    self._ref,
                    DCAT.centroid,
                    Literal(self.centroid, datatype=GEOSPARQL.asWKT),
                )
            )
