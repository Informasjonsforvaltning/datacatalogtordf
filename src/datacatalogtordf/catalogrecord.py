"""CatalogRecord module for mapping a catalogrecord to rdf.

This module contains methods for mapping a catalogrecord object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-katalog>`__

Example:
    >>> from datacatalogtordf import CatalogRecord
    >>>
    >>> catalogrecord = CatalogRecord()
    >>> catalogrecord.identifier = "http://example.com/catalogrecords/1"
    >>> catalogrecord.title = {"en": "Title of catalogrecord"}
    >>>
    >>> bool(catalogrecord.to_rdf())
    True

"""
from __future__ import annotations

from typing import List, Optional

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from .periodoftime import Date
from .resource import Resource
from .uri import URI

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class CatalogRecord:
    """A class representing a dcat:CatalogRecord.

    Ref: https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog_Record

    Attributes:
        identifier (URI): a URI uniquely identifying the catalog record
        title (dict): A name given to the record. key is language code.
        description (dict): A free-text account of the record. key is language code.
        listing_date (Date): The date of listing
        modification_date (Date): Most recent date on which the catalog entry \
            was changed
        primary_topic (Resource): The dcat:Resource (dataset or service) \
            described in the record.
        conforms_to (List[URI]): An established standard to which the described \
            resource conforms.
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_title",
        "_description",
        "_listing_date",
        "_modification_date",
        "_primary_topic",
        "_conforms_to",
    )

    _g: Graph
    _identifier: URI
    _title: dict
    _description: dict
    _listing_date: Date
    _modification_date: Date
    _primary_topic: Resource
    _conforms_to: List[str]

    def __init__(self) -> None:
        """Inits catalogrecord object with default values."""
        self.conforms_to = []

    @property
    def identifier(self: CatalogRecord) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: CatalogRecord, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def title(self: CatalogRecord) -> dict:
        """Title attribute."""
        return self._title

    @title.setter
    def title(self: CatalogRecord, title: dict) -> None:
        self._title = title

    @property
    def description(self: CatalogRecord) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self: CatalogRecord, description: dict) -> None:
        self._description = description

    @property
    def listing_date(self: CatalogRecord) -> str:
        """Get/set for listing_date."""
        return self._listing_date

    @listing_date.setter
    def listing_date(self: CatalogRecord, listing_date: str) -> None:
        self._listing_date = Date(listing_date)

    @property
    def modification_date(self: CatalogRecord) -> str:
        """Get/set for modification_date."""
        return self._modification_date

    @modification_date.setter
    def modification_date(self: CatalogRecord, modification_date: str) -> None:
        self._modification_date = Date(modification_date)

    @property
    def primary_topic(self: CatalogRecord) -> Resource:
        """Get/set for primary_topic."""
        return self._primary_topic

    @primary_topic.setter
    def primary_topic(self: CatalogRecord, primary_topic: Resource) -> None:
        self._primary_topic = primary_topic

    @property
    def conforms_to(self: CatalogRecord) -> List[str]:
        """Get/set for conforms_to."""
        return self._conforms_to

    @conforms_to.setter
    def conforms_to(self: CatalogRecord, conforms_to: List[str]) -> None:
        self._conforms_to = conforms_to

    # -
    def to_rdf(
        self: CatalogRecord, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the catalogrecord to rdf."""
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -
    def _to_graph(self: CatalogRecord) -> Graph:

        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("xsd", XSD)
        self._g.bind("foaf", FOAF)

        self._g.add((URIRef(self.identifier), RDF.type, DCAT.CatalogRecord))

        self._title_to_graph()
        self._description_to_graph()
        self._listing_date_to_graph()
        self._modification_date_to_graph()
        self._primary_topic_to_graph()
        self._conforms_to_to_graph()

        return self._g

    def _title_to_graph(self: CatalogRecord) -> None:
        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

    def _description_to_graph(self: CatalogRecord) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _listing_date_to_graph(self: CatalogRecord) -> None:
        if getattr(self, "listing_date", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.issued,
                    Literal(self.listing_date, datatype=XSD.date),
                )
            )

    def _modification_date_to_graph(self: CatalogRecord) -> None:
        if getattr(self, "modification_date", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.modified,
                    Literal(self.modification_date, datatype=XSD.date),
                )
            )

    def _primary_topic_to_graph(self: CatalogRecord) -> None:
        if getattr(self, "primary_topic", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    FOAF.primaryTopic,
                    URIRef(self.primary_topic.identifier),
                )
            )

    def _conforms_to_to_graph(self: CatalogRecord) -> None:
        if getattr(self, "conforms_to", None):
            for _standard in self.conforms_to:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.conformsTo,
                        URIRef(_standard),
                    )
                )
