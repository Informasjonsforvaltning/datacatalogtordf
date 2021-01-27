"""Agent module for mapping a agent to rdf.

This module contains methods for mapping a agent object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-distribusjon>`__

Example:
    >>> from datacatalogtordf import Agent, Dataset
    >>> dataset = Dataset()
    >>> dataset.identifier = "http://example.com/datasets/1"
    >>> # Create an agent:
    >>> agent = Agent()
    >>> agent.identifier = "http://example.com/agents/1"
    >>> agent.name = {"en": "James Bond", "nb": "Djeims Bånd"}
    >>> # Assigen the agent to the publisher property:
    >>> dataset.publisher = agent
    >>> bool(dataset.to_rdf())
    True
"""
from __future__ import annotations

from typing import Optional

from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, URIRef

from .uri import URI


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class Agent:
    """A class representing a foaf:Agent.

    Attributes:
        identifier (URI): A URI uniquely identifying the agent
        name (dict): A name given to the agent. key is langauge code
        organization_id (str): The organzation's identifier
        organization_type (URI): a link to a concept designating the type of the agent
    """

    slots = ("_identifier", "_name", "_organization_id", "_same_as")

    _identifier: URI
    _name: dict
    _organization_id: str
    _organization_type: URI
    _same_as: URI

    def __init__(self) -> None:
        """Inits an object with default values."""
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("foaf", FOAF)

    @property
    def identifier(self: Agent) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Agent, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def name(self: Agent) -> dict:
        """Name attribute."""
        return self._name

    @name.setter
    def name(self: Agent, name: dict) -> None:
        self._name = name

    @property
    def organization_id(self: Agent) -> str:
        """Organization attribute."""
        return self._organization_id

    @organization_id.setter
    def organization_id(self: Agent, organization_id: str) -> None:
        self._organization_id = organization_id

    @property
    def organization_type(self: Agent) -> str:
        """Type attribute."""
        return self._organization_type

    @organization_type.setter
    def organization_type(self: Agent, organization_type: str) -> None:
        self._organization_type = URI(organization_type)

    @property
    def same_as(self: Agent) -> str:
        """Get for same_as."""
        return self._same_as

    @same_as.setter
    def same_as(self: Agent, same_as: str) -> None:
        """Get for same_as."""
        self._same_as = URI(same_as)

    # -
    def to_rdf(
        self: Agent, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the agent to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -
    def _to_graph(self: Agent) -> Graph:

        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        self._g.add((_self, RDF.type, FOAF.Agent))

        if getattr(self, "name", None):
            for key in self.name:
                self._g.add(
                    (
                        _self,
                        FOAF.name,
                        Literal(self.name[key], lang=key),
                    )
                )

        if getattr(self, "organization_id", None):
            self._g.add(
                (
                    _self,
                    DCT.identifier,
                    Literal(self.organization_id),
                )
            )

        if getattr(self, "organization_type", None):
            self._g.add(
                (
                    _self,
                    DCT.type,
                    URIRef(self.organization_type),
                )
            )

        if getattr(self, "same_as", None):
            self._g.add((URIRef(self.identifier), OWL.sameAs, (URIRef(self._same_as))))

        return self._g
