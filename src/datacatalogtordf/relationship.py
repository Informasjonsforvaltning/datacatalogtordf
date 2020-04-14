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

from typing import TYPE_CHECKING

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
        identifier: an URI uniquely identifying the resource
        relation: an URI uniquely identifying related resource
        had_role: an URI identifying the role
    """

    slots = ("_identifier", "_relation", "_had_role", "_ref")

    _identifier: URI
    _relation: Resource
    _had_role: URI
    _ref: URIRef

    def __init__(self) -> None:
        """Inits an object with default values."""
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)

    @property
    def identifier(self: Relationship) -> URI:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Relationship, identifier: URI) -> None:
        self._identifier = identifier

    @property
    def had_role(self: Relationship) -> URI:
        """Get/set for had_role."""
        return self._had_role

    @had_role.setter
    def had_role(self: Relationship, had_role: URI) -> None:
        self._had_role = had_role

    @property
    def relation(self: Relationship) -> Resource:
        """Get/set for relation."""
        return self._relation

    @relation.setter
    def relation(self: Relationship, relation: Resource) -> None:
        self._relation = relation

    # -
    def to_rdf(self: Relationship, format: str = "turtle") -> str:
        """Maps the relationship to rdf.

        Args:
            format: a valid format. Default: turtle

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding="utf-8")

    # -
    def _to_graph(self: Relationship) -> Graph:

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

        self._g.add((self._ref, DCT.relation, URIRef(self.relation.identifier),))

    def _had_role_to_graph(self: Relationship) -> None:

        self._g.add((self._ref, DCAT.hadRole, URIRef(self.had_role),))
