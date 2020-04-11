"""URI helper module for very basic validation of a uri."""
from __future__ import annotations

from rdflib import Graph, Literal, RDF, URIRef

from .exceptions import InvalidURIError


class URI(str):
    r"""A helper class to validate a URI.

    If the string is serializable as an rdflib.URIRef,
    it is valid. Otherwise not.

    Essentially it is serializable if none of the following chars occurs::

    _invalid_uri_chars = '<>" {}|\\^`'

    Ref: https://github.com/RDFLib/rdflib/blob/master/rdflib/term.py#L75

    Example:
        >>> from datacatalogtordf import Dataset, URI
        >>>
        >>> dataset = Dataset()
        >>> dataset.identifier = URI("http://example.com/datasets/1")
        >>> dataset.identifier
        'http://example.com/datasets/1'
    """

    def __init__(self, link: str) -> None:
        """Validate a URI object."""
        try:
            self._is_valid_uri(link)
        except Exception as err:
            raise InvalidURIError(link, str(err))

    # -
    def _is_valid_uri(self: URI, link: str) -> None:
        """Perform basic validation of link."""
        _uriref = URIRef(link)
        _g = Graph()
        _g.add((_uriref, RDF.type, Literal(None)))
        _g.serialize(format="n3")
