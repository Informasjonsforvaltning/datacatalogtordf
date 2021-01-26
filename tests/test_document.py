"""Test cases for the document module."""
import pytest

from datacatalogtordf.document import Document


def test_instantiate_document() -> None:
    """It does not raise an exception."""
    try:
        _ = Document()
    except Exception:
        pytest.fail("Unexpected Exception ..")
