"""URI helper module for very basic validation of a uri."""
from __future__ import annotations

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
        if not _is_valid_uri(link):
            raise InvalidURIError(link, f"{link} is not a valid URI")


def _is_valid_uri(uri: str) -> bool:
    """Perform basic validation of link."""
    _invalid_uri_chars = '<>" {}|\\^`'

    for c in _invalid_uri_chars:
        if c in uri:
            return False
    return True
