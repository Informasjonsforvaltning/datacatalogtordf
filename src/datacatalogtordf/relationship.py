"""Relationship module for mapping a relationship to rdf.

This module contains methods for mapping a relationship object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-distribusjon>`__

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

from typing import Optional, TYPE_CHECKING

from rdflib import BNode, Graph, Namespace, RDF, URIRef

from .uri import URI

if TYPE_CHECKING:  # pragma: no cover
    from .resource import Resource

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Relationship:
    """A class representing a dcat:Relationship.

    Ref: `dcat:Relationship <https://www.w3.org/TR/vocab-dcat-2/#Class:Relationship>`_

    Attributes:
        identifier (URI): a URI uniquely identifying the resource
        relation (Resource): A URI uniquely identifying related resource
        had_role (URI): A URI identifying the role
    """

    slots = ("_g", "_identifier", "_relation", "_had_role", "_ref")

    _g: Graph
    _identifier: URI
    _relation: Resource
    _had_role: URI
    _ref: URIRef

    def __init__(self) -> None:
        """Inits an object with default values."""
        pass

    @property
    def identifier(self: Relationship) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Relationship, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def had_role(self: Relationship) -> str:
        """Get/set for had_role."""
        return self._had_role

    @had_role.setter
    def had_role(self: Relationship, had_role: str) -> None:
        self._had_role = URI(had_role)

    @property
    def relation(self: Relationship) -> Resource:
        """Get/set for relation."""
        return self._relation

    @relation.setter
    def relation(self: Relationship, relation: Resource) -> None:
        self._relation = relation

    # -
    def to_rdf(
        self: Relationship, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
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

        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)

        if getattr(self, "identifier", None):
            self._ref = URIRef(self.identifier)
        else:
            self._ref = BNode()
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
