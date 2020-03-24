"""Test cases for the URI module."""
import pytest

from datacatalogtordf import InvalidURIError, URI


def test_valid_uri() -> None:
    """It does not raise an exception."""
    _valid_uri = "http://example.com/uris/1"
    _ = URI(_valid_uri)


def test_valid_uri_as_str() -> None:
    """It does return the correct uri as str."""
    valid_uri = "http://example.com/uris/1"
    uri = URI(valid_uri)

    assert uri == valid_uri


def test_invalid_uri() -> None:
    """It does raise an InvalidURIError."""
    _invalid_uri = "http://example.com/an invalid path"
    with pytest.raises(InvalidURIError):
        _ = URI(_invalid_uri)
