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

from rdflib import FOAF, Namespace

from datacatalogtordf.uri import URI

DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Document:
    """A class representing a foaf:Document.

    Attributes:
        identifier (URI): A URI uniquely identifying the document
        title (dict): A title given to the document. key is langauge code
        language (str): The organzation's identifier
        format (URI): a link to a concept designating the type of the document
    """

    slots = ("_identifier", "_title", "_language", "_format")

    _identifier: URI
    _title: dict
    _language: str
    _format: URI
    _type: str

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = FOAF.Document
