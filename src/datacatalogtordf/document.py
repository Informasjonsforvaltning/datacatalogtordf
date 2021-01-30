"""Document module for mapping a document to rdf.

This module contains methods for mapping a document object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-distribusjon>`__

Example:
    >>> from datacatalogtordf import Document
    >>> # Create a document:
    >>> document = Document()
    >>> document.identifier = "http://example.com/documents/1"
    >>> document.title = {"en": "The Python Language Reference Manual"}
"""
from __future__ import annotations

from typing import Optional

from rdflib import BNode, DCTERMS, FOAF, Graph, Literal, Namespace, RDF, URIRef

from datacatalogtordf.uri import URI

DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Document:
    """A class representing a foaf:Document.

    Attributes:
        identifier (URI): A URI uniquely identifying the document
        title (dict): A title given to the document. key is langauge code
        language (str): A reference to the language which is used in the document
        format (str): A link to a concept designating the type of the document
    """

    slots = (
        "_identifier",
        "_title",
        "_language",
    )

    _identifier: URI
    _title: dict
    _language: str
    _type: str

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = FOAF.Document

    @property
    def identifier(self: Document) -> str:
        """Get for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Document, identifier: str) -> None:
        """Set for identifier."""
        self._identifier = URI(identifier)

    @property
    def title(self) -> dict:
        """Get for title attribute."""
        return self._title

    @title.setter
    def title(self, title: dict) -> None:
        """Set for title attribute."""
        self._title = title

    @property
    def language(self: Document) -> str:
        """Get for language."""
        return self._language

    @language.setter
    def language(self: Document, language: str) -> None:
        """Set for language."""
        self._language = URI(language)

    def to_rdf(
        self: Document, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the document to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self: Document) -> Graph:

        self._g = Graph()
        self._g.bind("dct", DCTERMS)
        self._g.bind("foaf", FOAF)

        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        self._g.add((_self, RDF.type, FOAF.Document))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        _self,
                        DCTERMS.title,
                        Literal(self.title[key], lang=key),
                    )
                )
        if getattr(self, "language", None):
            self._g.add(
                (
                    _self,
                    DCTERMS.language,
                    Literal(self.language, datatype=DCTERMS.LinguisticSystem),
                )
            )

        return self._g
