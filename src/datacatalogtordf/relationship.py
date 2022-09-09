"""Relationship module for mapping a relationship to rdf.

This module contains methods for mapping a relationship object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#klasse-relasjon>`__

Example:
    >>> from datacatalogtordf import Relationship
    >>>
    >>> relationship = Relationship()
    >>> relationship.identifier = "http://example.com/relations/1"
    >>> relationship.title = {"en": "Title of relationship"}
    >>>
    >>> bool(relationship.to_rdf())
    True
"""
from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING, Union

from rdflib import Graph, Namespace, RDF, URIRef
from skolemizer import Skolemizer  # type: ignore

from .uri import URI

if TYPE_CHECKING:  # pragma: no cover
    from .resource import Resource

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Relationship:
    """A class representing a dcat:Relationship.

    Ref: `dcat:Relationship <https://www.w3.org/TR/vocab-dcat-2/#Class:Relationship>`_
    """

    __slots__ = ("_g", "_identifier", "_relation", "_had_role", "_ref")

    _g: Graph
    _identifier: URI
    _relation: Resource
    _had_role: URI
    _ref: URIRef

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier

    @property
    def identifier(self: Relationship) -> str:
        """URI: a URI uniquely identifying the resource."""
        return self._identifier

    @identifier.setter
    def identifier(self: Relationship, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def had_role(self: Relationship) -> str:
        """URI: A URI identifying the role."""
        return self._had_role

    @had_role.setter
    def had_role(self: Relationship, had_role: str) -> None:
        self._had_role = URI(had_role)

    @property
    def relation(self: Relationship) -> Resource:
        """Resource: A URI uniquely identifying related resource."""
        return self._relation

    @relation.setter
    def relation(self: Relationship, relation: Resource) -> None:
        self._relation = relation

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
    def from_json(cls, json: Dict) -> Relationship:
        """Convert a JSON (dict).

        Args:
            json: A dict representing this class.

        Returns:
            Relationship: The object.
        """
        resource = cls()
        for key in json:
            is_private = key.startswith("_")
            if not is_private:
                v = json[key]

                attr = cls._attr_from_json(key, v)
                if attr is not None:
                    setattr(resource, key, attr)
                else:
                    setattr(resource, key, v)

        return resource

    @classmethod
    def _attr_from_json(cls: Any, attr: str, json_dict: Dict) -> Any:
        if attr == "relation":
            if (
                isinstance(json_dict, dict)
                and "_type" in json_dict.keys()
                and json_dict["_type"]
                in ["Catalog", "Dataset", "DatasetSeries", "DataService"]
            ):
                clazz = getattr(__import__("datacatalogtordf"), json_dict["_type"])
                return clazz.from_json(json_dict)

        return None

    def to_rdf(
        self: Relationship, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> Union[bytes, str]:
        """Maps the relationship to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -
    def _to_graph(self: Relationship) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)

        self._ref = URIRef(self.identifier)
        self._g.add((self._ref, RDF.type, DCAT.Relationship))

        if getattr(self, "relation", None):
            self._relation_to_graph()

        if getattr(self, "had_role", None):
            self._had_role_to_graph()

        return self._g

    def _relation_to_graph(self: Relationship) -> None:

        self._g.add(
            (
                self._ref,
                DCT.relation,
                URIRef(self.relation.identifier),
            )
        )

    def _had_role_to_graph(self: Relationship) -> None:

        self._g.add(
            (
                self._ref,
                DCAT.hadRole,
                URIRef(self.had_role),
            )
        )
