"""Location module for mapping a location to rdf.

This module contains methods for mapping a location object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#klasse-lokasjon>`__

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

from typing import Dict, Optional, Union

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from skolemizer import Skolemizer  # type: ignore

from .uri import URI

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
LOCN = Namespace("http://www.w3.org/ns/locn#")
GEOSPARQL = Namespace("http://www.opengis.net/ont/geosparql#")


class Location:
    """A class representing a dcat:Location.

    Ref: `dcat:Location <https://www.w3.org/TR/vocab-dcat-2/#Class:Location>`_
    """

    __slots__ = ("_g", "_identifier", "_geometry", "_bounding_box", "_centroid", "_ref")

    _g: Graph
    _identifier: URI
    _geometry: str
    _bounding_box: str
    _centroid: str
    _ref: URIRef

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier

        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("locn", LOCN)
        self._g.bind("geosparql", GEOSPARQL)

    @property
    def identifier(self: Location) -> str:
        """URI: an URI uniquely identifying the resource."""
        return self._identifier

    @identifier.setter
    def identifier(self: Location, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def geometry(self: Location) -> str:
        """str: Associates any resource with the corresponding geometry."""
        return self._geometry

    @geometry.setter
    def geometry(self: Location, geometry: str) -> None:
        self._geometry = geometry

    @property
    def bounding_box(self: Location) -> str:
        """str: The geographic bounding box of a resource."""
        return self._bounding_box

    @bounding_box.setter
    def bounding_box(self: Location, bounding_box: str) -> None:
        self._bounding_box = bounding_box

    @property
    def centroid(self: Location) -> str:
        """str: The geographic center (centroid) of a resource."""
        return self._centroid

    @centroid.setter
    def centroid(self: Location, centroid: str) -> None:
        self._centroid = centroid

    # -
    def to_json(self) -> Dict:
        """Convert the Resource to a json / dict. It will omit the non-initalized fields.

        Returns:
            Dict: The json representation of this instance.
        """
        output = {"_type": type(self).__name__}
        # Add ins for optional top level attributes
        for k in dir(self):
            try:
                v = getattr(self, k)
                is_method = callable(v)
                is_private = k.startswith("_")
                if is_method or is_private:
                    continue

                to_json = hasattr(v, "to_json") and callable(getattr(v, "to_json"))
                output[k] = v.to_json() if to_json else v

            except AttributeError:
                continue

        return output

    @classmethod
    def from_json(cls, json: Dict) -> Location:
        """Convert a JSON (dict).

        Args:
            json: A dict representing this class.

        Returns:
            Location: The object.
        """
        resource = cls()
        for key in json:
            is_private = key.startswith("_")
            if not is_private:
                setattr(resource, key, json[key])

        return resource

    def to_rdf(
        self: Location, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> Union[bytes, str]:
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

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        self._ref = URIRef(self.identifier)
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
