"""Agent module for mapping a agent to rdf.

This module contains methods for mapping a agent object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#klasse-aktor>`__

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

from typing import Dict, Optional, Union

from rdflib import Graph, Literal, Namespace, OWL, RDF, URIRef
from skolemizer import Skolemizer  # type: ignore

from .uri import URI

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class Agent:
    """A class representing a foaf:Agent.

    Args:
        identifier (URI): the identifier of the dataset.
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_name",
        "_organization_id",
        "_organization_type",
        "_same_as",
    )

    _g: Graph
    _identifier: URI
    _name: Dict[str, str]
    _organization_id: str
    _organization_type: URI
    _same_as: URI

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier

        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("foaf", FOAF)

    @property
    def identifier(self: Agent) -> str:
        """URI: A URI uniquely identifying the agent."""
        return self._identifier

    @identifier.setter
    def identifier(self: Agent, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def name(self: Agent) -> Dict[str, str]:
        """Dict[str, str]: A name given to the agent. key is langauge code."""
        return self._name

    @name.setter
    def name(self: Agent, name: Dict[str, str]) -> None:
        self._name = name

    @property
    def organization_id(self: Agent) -> str:
        """str: The organzation's identifier."""
        return self._organization_id

    @organization_id.setter
    def organization_id(self: Agent, organization_id: str) -> None:
        self._organization_id = organization_id

    @property
    def organization_type(self: Agent) -> str:
        """URI: Link to a concept designating the type of the agent."""
        return self._organization_type

    @organization_type.setter
    def organization_type(self: Agent, organization_type: str) -> None:
        self._organization_type = URI(organization_type)

    @property
    def same_as(self: Agent) -> str:
        """URI: Link to another resource that is the same as this one."""
        return self._same_as

    @same_as.setter
    def same_as(self: Agent, same_as: str) -> None:
        self._same_as = URI(same_as)

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
    def from_json(cls, json: Dict) -> Agent:
        """Convert a JSON (dict).

        Args:
            json: A dict representing this class

        Returns:
            Agent: The object
        """
        resource = cls()
        for key in json:
            is_private = key.startswith("_")
            if not is_private:
                setattr(resource, key, json[key])

        return resource

    def to_rdf(
        self: Agent, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> Union[bytes, str]:
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

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        self._g.add((URIRef(self.identifier), RDF.type, FOAF.Agent))

        if getattr(self, "name", None):
            for key in self.name:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        FOAF.name,
                        Literal(self.name[key], lang=key),
                    )
                )

        if getattr(self, "organization_id", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.organization_id),
                )
            )

        if getattr(self, "organization_type", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.type,
                    URIRef(self.organization_type),
                )
            )

        if getattr(self, "same_as", None):
            self._g.add((URIRef(self.identifier), OWL.sameAs, (URIRef(self._same_as))))

        return self._g
