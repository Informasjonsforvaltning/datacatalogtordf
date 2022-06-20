"""Document module for mapping a document to rdf.

This module contains methods for mapping a document object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#klasse-dokument>`__

Example:
    >>> from datacatalogtordf import Document
    >>> # Create a document:
    >>> document = Document()
    >>> document.identifier = "http://example.com/documents/1"
    >>> document.title = {"en": "The Python Language Reference Manual"}
"""
from __future__ import annotations

from typing import Dict, Optional, Union

from rdflib import DCTERMS, FOAF, Graph, Literal, Namespace, RDF, URIRef
from skolemizer import Skolemizer

from datacatalogtordf.uri import URI

DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Document:
    """A class representing a foaf:Document."""

    slots = (
        "_identifier",
        "_title",
        "_language",
    )

    _identifier: URI
    _title: Dict[str, str]
    _language: str
    _type: str

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        self._type = FOAF.Document

    @property
    def identifier(self: Document) -> str:
        """URI: A URI uniquely identifying the document."""
        return self._identifier

    @identifier.setter
    def identifier(self: Document, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def title(self) -> Dict[str, str]:
        """Dict[str, str]: A title given to the document. key is langauge code."""
        return self._title

    @title.setter
    def title(self, title: Dict[str, str]) -> None:
        self._title = title

    @property
    def language(self: Document) -> str:
        """str: A reference to the language which is used in the document."""
        return self._language

    @language.setter
    def language(self: Document, language: str) -> None:
        self._language = URI(language)

    def to_rdf(
        self: Document, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> Union[bytes, str]:
        """Maps the document to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self: Document) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        self._g = Graph()
        self._g.bind("dct", DCTERMS)
        self._g.bind("foaf", FOAF)

        _self = URIRef(self.identifier)

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
