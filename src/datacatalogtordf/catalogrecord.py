"""CatalogRecord module for mapping a catalogrecord to rdf.

This module contains methods for mapping a catalogrecord object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#klasse-katalogpost>`__

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

from typing import Any, Dict, List, Optional, Union

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from skolemizer import Skolemizer  # type: ignore

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

    Args:
        identifier (URI): the identifier of the dataset-series.
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
    _title: Dict[str, str]
    _description: Dict[str, str]
    _listing_date: Date
    _modification_date: Date
    _primary_topic: Resource
    _conforms_to: List[str]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits catalogrecord object with default values."""
        if identifier:
            self.identifier = identifier
        self.conforms_to = []

    @property
    def identifier(self: CatalogRecord) -> str:
        """URI: a URI uniquely identifying the catalog record."""
        return self._identifier

    @identifier.setter
    def identifier(self: CatalogRecord, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def title(self: CatalogRecord) -> Dict[str, str]:
        """Dict[str, str]: A name given to the record. key is language code."""
        return self._title

    @title.setter
    def title(self: CatalogRecord, title: Dict[str, str]) -> None:
        self._title = title

    @property
    def description(self: CatalogRecord) -> Dict[str, str]:
        """Dict[str, str]: A free-text account of the record. key is language code."""
        return self._description

    @description.setter
    def description(self: CatalogRecord, description: Dict[str, str]) -> None:
        self._description = description

    @property
    def listing_date(self: CatalogRecord) -> str:
        """Date: The date of listing."""
        return self._listing_date

    @listing_date.setter
    def listing_date(self: CatalogRecord, listing_date: str) -> None:
        self._listing_date = Date(listing_date)

    @property
    def modification_date(self: CatalogRecord) -> str:
        """Date: Most recent date on which the catalog entry was changed."""
        return self._modification_date

    @modification_date.setter
    def modification_date(self: CatalogRecord, modification_date: str) -> None:
        self._modification_date = Date(modification_date)

    @property
    def primary_topic(self: CatalogRecord) -> Resource:
        """Resource: The dcat:Resource (dataset or service) described in the record."""
        # noqa: B950
        return self._primary_topic

    @primary_topic.setter
    def primary_topic(self: CatalogRecord, primary_topic: Resource) -> None:
        self._primary_topic = primary_topic

    @property
    def conforms_to(self: CatalogRecord) -> List[str]:
        """List[URI]: An established standard to which the described resource conforms."""
        return self._conforms_to

    @conforms_to.setter
    def conforms_to(self: CatalogRecord, conforms_to: List[str]) -> None:
        # Validate conforms_to URIs:
        for string in conforms_to:
            URI(string)

        self._conforms_to = conforms_to

    # -
    def to_json(self) -> Dict:
        """Convert the Resource to a json / dict. It will omit the non-initalized fields.

        Returns:
            Dict: The json representation of this instance.
        """
        output: Dict = {"_type": type(self).__name__}
        # Add ins for optional top level attributes
        for k in dir(self):
            try:
                v = getattr(self, k)
                is_method = callable(v)
                is_private = k.startswith("_")
                if is_method or is_private:
                    continue

                if isinstance(v, list):
                    output[k] = []
                    for i in v:
                        to_json = hasattr(i, "to_json") and callable(
                            getattr(i, "to_json")
                        )
                        output[k].append(i.to_json() if to_json else i)
                else:
                    to_json = hasattr(v, "to_json") and callable(getattr(v, "to_json"))
                    output[k] = v.to_json() if to_json else v

            except AttributeError:
                continue

        return output

    @classmethod
    def from_json(cls, json: Dict) -> CatalogRecord:
        """Convert a JSON (dict).

        Args:
            json: A dict representing this class.

        Returns:
            CatalogRecord: The object.
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
    def _attr_from_json(cls, attr: str, json_dict: Dict) -> Any:
        if attr == "primary_topic":
            for class_name in ["Catalog", "Dataset", "DatasetSeries", "DataService"]:
                clazz = getattr(__import__("datacatalogtordf"), class_name)
                return clazz.from_json(json_dict)

        return None

    def to_rdf(
        self: CatalogRecord, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> Union[bytes, str]:
        """Maps the catalogrecord to rdf."""
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -
    def _to_graph(self: CatalogRecord) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

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

            if not getattr(self.primary_topic, "identifier", None):
                self.primary_topic.identifier = Skolemizer.add_skolemization()

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
