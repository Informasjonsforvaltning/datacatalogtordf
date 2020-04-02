"""Resource module for mapping a sub-classes to rdf.

This module contains methods for mapping a sub-class objects to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/>`_

Refer to sub-class for typical usage examples.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from concepttordf import Contact
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

from .uri import URI


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
PROV = Namespace("http://www.w3.org/ns/prov#")


class InvalidDateError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        str -- input str in which the error occurred
        message -- explanation of the error
    """

    __slots__ = ()

    def __init__(self, string: str, message: str) -> None:
        """Inits the exception."""
        self.str = str
        self.message = message


class Resource(ABC):
    """An abstract class representing a dcat:Resource.

    Ref: `dcat:Resource <https://www.w3.org/TR/vocab-dcat-2/#Class:Resource>`_.

    Attributes:
        identifier: an URI uniquely identifying the resource
        publisher: an URI uniquely identifying the publisher of the resource
        title: a dict with title in multiple languages
    """

    # Use slots to save memory, faster access and restrict attribute creation
    __slots__ = (
        "_g",
        "_accessRights",
        "_conformsTo",
        "_contactpoint",
        "_creator",
        "_description",
        "_title",
        "_release_date",
        "_modification_date",
        "_language",
        "_publisher",
        "_identifier",
        "_theme",
        "_type_genre",
        "_resource_relation",
        "_qualified_relation",
        "_keyword_tag",
        "_landing_page",
        "_qualified_attributions",
        "_license",
        "_rights",
        "_has_policy",
        "_is_referenced_by",
    )

    # Types
    _accessRights: str  # 6.4.1
    _conformsTo: List[str]  # 6.4.2
    _contactpoint: Contact  # 6.4.3
    _creator: str  # 6.4.4
    _description: dict  # 6.4.5
    _title: dict  # 6.4.6
    _release_date: str  # 6.4.7
    _modification_date: str  # 6.4.8
    _language: str  # 6.4.9
    _publisher: str  # 6.4.10
    _identifier: str  # 6.4.11
    _theme: List[str]  # 6.4.12
    _type_genre: str  # 6.4.13
    _resource_relation: Resource  # 6.4.14
    _qualified_relation: str  # 6.4.15
    _keyword_tag: dict  # 6.4.16
    _landing_page: List[str]  # 6.4.17
    _qualified_attributions: List[dict]  # 6.4.18
    _license: str  # 6.4.19
    _rights: str  # 6.4.20
    _has_policy: str  # 6.4.21
    _is_referenced_by: List[Resource]  # 6.4.22

    @abstractmethod
    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = DCAT.Resource
        # Initalize lists:
        self.conformsTo = list()
        self.theme = list()
        self.is_referenced_by = list()
        self.qualified_attributions = list()
        self.landing_page = list()
        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("odrl", ODRL)
        self._g.bind("xsd", XSD)
        self._g.bind("prov", PROV)

    @property
    def identifier(self: Resource) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Resource, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def publisher(self: Resource) -> str:
        """Get/set for publisher."""
        return self._publisher

    @publisher.setter
    def publisher(self: Resource, publisher: str) -> None:
        self._publisher = URI(publisher)

    @property
    def title(self: Resource) -> dict:
        """Title attribute.

        Returns:
            the title as dictionary
        """
        return self._title

    @title.setter
    def title(self: Resource, title: dict) -> None:
        self._title = title

    @property
    def description(self: Resource) -> dict:
        """Description attribute.

        Returns:
            the description as dictionary
        """
        return self._description

    @description.setter
    def description(self: Resource, description: dict) -> None:
        """Title attribute setter."""
        self._description = description

    @property
    def accessRights(self: Resource) -> str:
        """Get/set for accessRights."""
        return self._accessRights

    @accessRights.setter
    def accessRights(self: Resource, accessRights: str) -> None:
        self._accessRights = URI(accessRights)

    @property
    def conformsTo(self: Resource) -> List[str]:
        """Get/set for conformsTo."""
        return self._conformsTo

    @conformsTo.setter
    def conformsTo(self: Resource, conformsTo: List[str]) -> None:
        self._conformsTo = conformsTo

    @property
    def theme(self: Resource) -> List[str]:
        """Get/set for theme."""
        return self._theme

    @theme.setter
    def theme(self: Resource, theme: List[str]) -> None:
        self._theme = theme

    @property
    def contactpoint(self: Resource) -> Contact:
        """Get/set for contactpoint."""
        return self._contactpoint

    @contactpoint.setter
    def contactpoint(self: Resource, contactpoint: Contact) -> None:
        self._contactpoint = contactpoint

    @property
    def creator(self: Resource) -> str:
        """Get/set for creator."""
        return self._creator

    @creator.setter
    def creator(self: Resource, creator: str) -> None:
        self._creator = URI(creator)

    @property
    def has_policy(self: Resource) -> str:
        """Get/set for has_policy."""
        return self._has_policy

    @has_policy.setter
    def has_policy(self: Resource, has_policy: str) -> None:
        self._has_policy = URI(has_policy)

    @property
    def is_referenced_by(self: Resource) -> List[Resource]:
        """Get/set for is_referenced_by."""
        return self._is_referenced_by

    @is_referenced_by.setter
    def is_referenced_by(self: Resource, is_referenced_by: List[Resource]) -> None:
        self._is_referenced_by = is_referenced_by

    @property
    def release_date(self: Resource) -> str:
        """Get/set for release_date."""
        return self._release_date

    @release_date.setter
    def release_date(self: Resource, release_date: str) -> None:
        # Try to convert release_date to date:
        try:
            _date = datetime.strptime(release_date, "%Y-%m-%d")
            self._release_date = _date.strftime("%Y-%m-%d")
        except ValueError:
            raise InvalidDateError(release_date, "String is not a date")

    @property
    def modification_date(self: Resource) -> str:
        """Get/set for modification_date."""
        return self._modification_date

    @modification_date.setter
    def modification_date(self: Resource, modification_date: str) -> None:
        # Try to convert release_date to date:
        try:
            _date = datetime.strptime(modification_date, "%Y-%m-%d")
            self._modification_date = _date.strftime("%Y-%m-%d")
        except Exception:
            raise InvalidDateError(modification_date, "String is not a date")

    @property
    def type_genre(self: Resource) -> str:
        """Get/set for type_genre."""
        return self._type_genre

    @type_genre.setter
    def type_genre(self: Resource, type_genre: str) -> None:
        self._type_genre = URI(type_genre)

    @property
    def qualified_attributions(self: Resource) -> List[dict]:
        """Get/set for qualified_attributions."""
        return self._qualified_attributions

    @qualified_attributions.setter
    def qualified_attributions(
        self: Resource, qualified_attributions: List[dict]
    ) -> None:
        self._qualified_attributions = qualified_attributions

    @property
    def landing_page(self: Resource) -> List[str]:
        """Get/set for landing_page."""
        return self._landing_page

    @landing_page.setter
    def landing_page(self: Resource, landing_page: List[str]) -> None:
        self._landing_page = landing_page

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

        Example:
            >>> from datacatalogtordf import Catalog
            >>>
            >>> catalog = Catalog()
            >>> catalog.identifier = "http://example.com/catalogs/1"
            >>> catalog.title = {'en': 'Title of catalog'}
            >>> bool(catalog.to_rdf())
            True
        """
        return self._to_graph().serialize(format=format, encoding="utf-8")

    # -
    def _to_graph(self: Resource) -> Graph:

        self._publisher_to_graph()
        self._title_to_graph()
        self._accessRights_to_graph()
        self._conformsTo_to_graph()
        self._description_to_graph()
        self._theme_to_graph()
        self._contactpoint_to_graph()
        self._creator_to_graph()
        self._has_policy_to_graph()
        self._is_referenced_by_to_graph()
        self._release_date_to_graph()
        self._modification_date_to_graph()
        self._type_genre_to_graph()
        self._qualified_attributions_to_graph()
        self._landing_page_to_graph()

        return self._g

    def _publisher_to_graph(self: Resource) -> None:
        if getattr(self, "publisher", None):
            self._g.add(
                (URIRef(self.identifier), DCT.publisher, URIRef(self.publisher))
            )

    def _title_to_graph(self: Resource) -> None:
        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

    def _accessRights_to_graph(self: Resource) -> None:
        if getattr(self, "accessRights", None):
            self._g.add(
                (URIRef(self.identifier), DCT.accessRights, URIRef(self.accessRights))
            )

    def _conformsTo_to_graph(self: Resource) -> None:
        if getattr(self, "conformsTo", None):
            for _c in self.conformsTo:
                _uri = URI(_c)
                self._g.add((URIRef(self.identifier), DCT.conformsTo, URIRef(_uri)))

    def _description_to_graph(self: Resource) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _theme_to_graph(self: Resource) -> None:
        if getattr(self, "theme", None):
            for _t in self.theme:
                _uri = URI(_t)
                self._g.add((URIRef(self.identifier), DCAT.theme, URIRef(_uri)))

    def _contactpoint_to_graph(self: Resource) -> None:
        if getattr(self, "contactpoint", None):
            contact = self.contactpoint
            contactPoint = BNode()
            for _s, p, o in contact._to_graph().triples((None, None, None)):
                self._g.add((contactPoint, p, o))
            self._g.add((URIRef(self.identifier), DCAT.contactPoint, contactPoint))

    def _creator_to_graph(self: Resource) -> None:
        if getattr(self, "creator", None):
            self._g.add((URIRef(self.identifier), DCT.creator, URIRef(self.creator)))

    def _has_policy_to_graph(self: Resource) -> None:
        if getattr(self, "has_policy", None):
            self._g.add(
                (URIRef(self.identifier), ODRL.hasPolicy, URIRef(self.has_policy))
            )

    def _is_referenced_by_to_graph(self: Resource) -> None:
        if getattr(self, "is_referenced_by", None):
            for _i in self.is_referenced_by:
                _uri = URI(_i.identifier)
                self._g.add((URIRef(self.identifier), DCT.isReferencedBy, URIRef(_uri)))

    def _release_date_to_graph(self: Resource) -> None:
        if getattr(self, "release_date", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.issued,
                    Literal(self.release_date, datatype=XSD.date),
                )
            )

    def _modification_date_to_graph(self: Resource) -> None:
        if getattr(self, "modification_date", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.modified,
                    Literal(self.modification_date, datatype=XSD.date),
                )
            )

    def _type_genre_to_graph(self: Resource) -> None:
        if getattr(self, "type_genre", None):
            self._g.add((URIRef(self.identifier), DCT.type, URIRef(self.type_genre)))

    def _qualified_attributions_to_graph(self: Resource) -> None:
        if getattr(self, "qualified_attributions", None):
            qa = BNode()
            for _qa in self.qualified_attributions:
                self._g.add((qa, RDF.type, PROV.Attribution))
                _uri = URI(_qa["agent"])
                self._g.add((qa, PROV.agent, URIRef(_uri)))
                _uri = URI(_qa["hadrole"])
                self._g.add((qa, DCAT.hadRole, URIRef(_uri)))
                self._g.add((URIRef(self.identifier), PROV.qualifiedAttribution, qa))

    def _landing_page_to_graph(self: Resource) -> None:
        if getattr(self, "landing_page", None):
            for _lp in self.landing_page:
                _uri = URI(_lp)
                self._g.add((URIRef(self.identifier), DCAT.landingPage, URIRef(_uri)))
