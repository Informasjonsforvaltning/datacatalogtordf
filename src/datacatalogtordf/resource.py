"""Resource module for mapping a sub-classes to rdf.

This module contains methods for mapping a sub-class objects to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/>`_

Refer to sub-class for typical usage examples.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, TYPE_CHECKING, Union

from concepttordf import Contact
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef
from rdflib.term import Identifier

from .agent import Agent
from .periodoftime import Date
from .uri import URI

if TYPE_CHECKING:  # pragma: no cover
    from .relationship import Relationship  # pytype: disable=pyi-error


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
PROV = Namespace("http://www.w3.org/ns/prov#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class Resource(ABC):
    """An abstract class representing a dcat:Resource.

    Ref: `dcat:Resource <https://www.w3.org/TR/vocab-dcat-2/#Class:Resource>`_.
    """

    # Use slots to save memory, faster access and restrict attribute creation
    __slots__ = (
        "_g",
        "_access_rights",
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
        "_keyword",
        "_landing_page",
        "_qualified_attributions",
        "_license",
        "_rights",
        "_has_policy",
        "_is_referenced_by",
        "_prev",
    )

    # Types
    _g: Graph
    _access_rights: URI  # 6.4.1
    _conformsTo: List[str]  # 6.4.2
    _contactpoint: Contact  # 6.4.3
    _creator: URI  # 6.4.4
    _description: Dict[str, str]  # 6.4.5
    _title: Dict[str, str]  # 6.4.6
    _release_date: Date  # 6.4.7
    _modification_date: Date  # 6.4.8
    _language: List[str]  # 6.4.9
    _publisher: Union[Agent, str]  # 6.4.10
    _identifier: URI  # 6.4.11
    _theme: List[str]  # 6.4.12
    _type_genre: URI  # 6.4.13
    _resource_relation: List[str]  # 6.4.14
    _qualified_relation: List[Relationship]  # 6.4.15
    _keyword: Dict[str, str]  # 6.4.16
    _landing_page: List[str]  # 6.4.17
    _qualified_attributions: List[Dict]  # 6.4.18
    _license: URI  # 6.4.19
    _rights: URI  # 6.4.20
    _has_policy: URI  # 6.4.21
    _is_referenced_by: List[Resource]  # 6.4.22
    _prev: Resource  # 6.4.33

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
        self.language = list()
        self.resource_relation = list()
        self.qualified_relation = list()

    @property
    def identifier(self: Resource) -> str:
        """URI: A URI uniquely identifying the resource."""
        return self._identifier

    @identifier.setter
    def identifier(self: Resource, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def publisher(self: Resource) -> Union[Agent, str]:
        """Union[Agent, str]: A URI uniquely identifying the publisher of the resource."""
        return self._publisher

    @publisher.setter
    def publisher(self: Resource, publisher: Union[Agent, str]) -> None:
        self._publisher = publisher

    @property
    def title(self: Resource) -> Dict[str, str]:
        """Dict[str, str]:  A name given to the item. key is langauge code."""
        return self._title

    @title.setter
    def title(self: Resource, title: Dict[str, str]) -> None:
        self._title = title

    @property
    def description(self: Resource) -> Dict[str, str]:
        """Dict[str, str]: A free-text account of the item. key is language code."""
        return self._description

    @description.setter
    def description(self: Resource, description: Dict[str, str]) -> None:
        self._description = description

    @property
    def access_rights(self: Resource) -> str:
        """URI: A link to information about who can access the resource or an indication of its security status."""  # noqa: B950
        return self._access_rights

    @access_rights.setter
    def access_rights(self: Resource, access_rights: str) -> None:
        self._access_rights = URI(access_rights)

    @property
    def conformsTo(self: Resource) -> List[str]:
        """List[URI]: A list of links to established standards to which the described resource conforms."""  # noqa: B950
        return self._conformsTo

    @conformsTo.setter
    def conformsTo(self: Resource, conformsTo: List[str]) -> None:
        self._conformsTo = conformsTo

    @property
    def theme(self: Resource) -> List[str]:
        """List[URI]: A list of links to categories of the resource."""
        return self._theme

    @theme.setter
    def theme(self: Resource, theme: List[str]) -> None:
        self._theme = theme

    @property
    def contactpoint(self: Resource) -> Contact:
        """Contact: Relevant contact information for the cataloged resource."""  # noqa: B950
        return self._contactpoint

    @contactpoint.setter
    def contactpoint(self: Resource, contactpoint: Contact) -> None:
        self._contactpoint = contactpoint

    @property
    def creator(self: Resource) -> str:
        """URI: Link to the entity responsible for producing the resource."""
        return self._creator

    @creator.setter
    def creator(self: Resource, creator: str) -> None:
        self._creator = URI(creator)

    @property
    def has_policy(self: Resource) -> str:
        """URI: A link to an ODRL conformant policy expressing the rights associated with the resource."""  # noqa: B950
        return self._has_policy

    @has_policy.setter
    def has_policy(self: Resource, has_policy: str) -> None:
        self._has_policy = URI(has_policy)

    @property
    def is_referenced_by(self: Resource) -> List[Resource]:
        """List[Resource]: A list of related resources, such as a publication, that references, cites, or otherwise points to the cataloged resource."""  # noqa: B950
        return self._is_referenced_by

    @is_referenced_by.setter
    def is_referenced_by(self: Resource, is_referenced_by: List[Resource]) -> None:
        self._is_referenced_by = is_referenced_by

    @property
    def release_date(self: Resource) -> str:
        """Date: Date of formal issuance (e.g., publication) of the item."""
        return self._release_date

    @release_date.setter
    def release_date(self: Resource, release_date: str) -> None:
        self._release_date = Date(release_date)

    @property
    def modification_date(self: Resource) -> str:
        """Date: Most recent date on which the item was changed, updated or modified."""
        return self._modification_date

    @modification_date.setter
    def modification_date(self: Resource, modification_date: str) -> None:
        self._modification_date = Date(modification_date)

    @property
    def type_genre(self: Resource) -> str:
        """URI:  A link to the nature or genre of the resource."""
        return self._type_genre

    @type_genre.setter
    def type_genre(self: Resource, type_genre: str) -> None:
        self._type_genre = URI(type_genre)

    @property
    def qualified_attributions(self: Resource) -> List[Dict]:
        """List[Dict]: List of links to an Agent having some form of responsibility for the resource."""  # noqa: B950
        return self._qualified_attributions

    @qualified_attributions.setter
    def qualified_attributions(
        self: Resource, qualified_attributions: List[Dict]
    ) -> None:
        self._qualified_attributions = qualified_attributions

    @property
    def landing_page(self: Resource) -> List[str]:
        """List[URI]: A list of links to web pages that can be navigated to in a Web browser to gain access to the catalog, a dataset, its distributions and/or additional information."""  # noqa: B950
        return self._landing_page

    @landing_page.setter
    def landing_page(self: Resource, landing_page: List[str]) -> None:
        self._landing_page = landing_page

    @property
    def license(self: Resource) -> str:
        """URI:	A link to a legal document under which the resource is made available."""
        return self._license

    @license.setter
    def license(self: Resource, license: str) -> None:
        self._license = URI(license)

    @property
    def language(self: Resource) -> List[str]:
        """List[str]: A list of links to languages of the item."""
        return self._language

    @language.setter
    def language(self: Resource, language: List[str]) -> None:
        self._language = language

    @property
    def resource_relation(self: Resource) -> List[str]:
        """List[URI]: A list of links to resources with an unspecified relationship to the cataloged item."""  # noqa: B950
        return self._resource_relation

    @resource_relation.setter
    def resource_relation(self: Resource, resource_relation: List[str]) -> None:
        self._resource_relation = resource_relation

    @property
    def rights(self: Resource) -> str:
        """URI: A link to a statement that concerns all rights not addressed with dct:license or dct:accessRights, such as copyright statements."""  # noqa: B950
        return self._rights

    @rights.setter
    def rights(self: Resource, rights: str) -> None:
        self._rights = URI(rights)

    @property
    def keyword(self: Resource) -> Dict[str, str]:
        """Dict[str, str]: A keyword or tag describing the resource. key is language code."""
        return self._keyword

    @keyword.setter
    def keyword(self: Resource, keyword: Dict[str, str]) -> None:
        self._keyword = keyword

    @property
    def qualified_relation(self: Resource) -> List[Relationship]:
        """List[Relationship]: A list of links to a description of a relationship with another resource."""  # noqa: B950
        return self._qualified_relation

    @qualified_relation.setter
    def qualified_relation(
        self: Resource, qualified_relation: List[Relationship]
    ) -> None:
        self._qualified_relation = qualified_relation

    @property
    def prev(self: Resource) -> Resource:
        """Resource: The previous resource in an ordered collection or series of resources."""
        return self._prev

    @prev.setter
    def prev(self: Resource, prev: Resource) -> None:
        self._prev = prev

    # -
    def to_rdf(
        self: Resource, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> Union[bytes, str]:
        """Maps the distribution to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format: a valid format.
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a bytes literal according to format.

        Example:
            >>> from datacatalogtordf import Catalog
            >>>
            >>> catalog = Catalog()
            >>> catalog.identifier = "http://example.com/catalogs/1"
            >>> catalog.title = {'en': 'Title of catalog'}
            >>> bool(catalog.to_rdf())
            True
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -
    def _to_graph(self: Resource) -> Graph:

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("odrl", ODRL)
        self._g.bind("xsd", XSD)
        self._g.bind("prov", PROV)
        self._g.bind("foaf", FOAF)

        self._publisher_to_graph()
        self._title_to_graph()
        self._access_rights_to_graph()
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
        self._license_to_graph()
        self._language_to_graph()
        self._resource_relation_to_graph()
        self._rights_to_graph()
        self._keyword_to_graph()
        self._qualified_relation_to_graph()
        self._prev_to_graph()

        return self._g

    def _publisher_to_graph(self: Resource) -> None:
        if getattr(self, "publisher", None):
            if type(self.publisher) is str:
                self._g.add(
                    (URIRef(self.identifier), DCT.publisher, URIRef(self.publisher))
                )
            elif type(self.publisher) is Agent:
                _agent: Identifier
                if getattr(self.publisher, "identifier", None):
                    _agent = URIRef(self.publisher.identifier)
                else:
                    _agent = BNode()

                for _s, p, o in self.publisher._to_graph().triples((None, None, None)):
                    self._g.add((_agent, p, o))
                self._g.add((URIRef(self.identifier), DCT.publisher, _agent))

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

    def _access_rights_to_graph(self: Resource) -> None:
        if getattr(self, "access_rights", None):
            self._g.add(
                (URIRef(self.identifier), DCT.accessRights, URIRef(self.access_rights))
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

    def _license_to_graph(self: Resource) -> None:
        if getattr(self, "license", None):
            self._g.add((URIRef(self.identifier), DCT.license, URIRef(self.license)))

    def _language_to_graph(self: Resource) -> None:
        if getattr(self, "language", None):
            for _l in self.language:
                _uri = URI(_l)
                self._g.add((URIRef(self.identifier), DCT.language, URIRef(_uri)))

    def _resource_relation_to_graph(self: Resource) -> None:
        if getattr(self, "resource_relation", None):
            for _l in self.resource_relation:
                _uri = URI(_l)
                self._g.add((URIRef(self.identifier), DCT.relation, URIRef(_uri)))

    def _rights_to_graph(self: Resource) -> None:
        if getattr(self, "rights", None):
            self._g.add((URIRef(self.identifier), DCT.rights, URIRef(self.rights)))

    def _keyword_to_graph(self: Resource) -> None:
        if getattr(self, "keyword", None):
            for key in self.keyword:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.keyword,
                        Literal(self.keyword[key], lang=key),
                    )
                )

    def _qualified_relation_to_graph(self: Resource) -> None:
        if getattr(self, "qualified_relation", None):
            for _qr in self.qualified_relation:
                _relation = _qr
                _relationship = BNode()
                for _s, p, o in _relation._to_graph().triples((None, None, None)):
                    self._g.add((_relationship, p, o))
                self._g.add(
                    (URIRef(self.identifier), DCAT.qualifiedRelation, _relationship)
                )

    def _prev_to_graph(self: Resource) -> None:
        if getattr(self, "prev", None):
            self._g.add(
                (URIRef(self.identifier), DCAT.prev, URIRef(self.prev.identifier))
            )
