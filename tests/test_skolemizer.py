"""Test cases for the skolemizer module."""
import os

from datacatalogtordf.skolemizer import Skolemizer

"""
A test class for testing the class InformationModel.

"""


def test_add_skolemization() -> None:
    """Tests skolemization."""
    skolemization1 = Skolemizer.add_skolemization()
    skolemization2 = Skolemizer.add_skolemization()

    assert skolemization1.startswith(
        Skolemizer.baseurl_default_value + ".well-known/skolem/"
    )
    assert Skolemizer.has_skolemization_morfologi(skolemization1)
    assert Skolemizer.is_exact_skolemization(skolemization1)

    assert skolemization2.startswith(
        Skolemizer.baseurl_default_value + ".well-known/skolem/"
    )
    assert Skolemizer.has_skolemization_morfologi(skolemization2)
    assert Skolemizer.is_exact_skolemization(skolemization2)


def test_get_baseurl() -> None:
    """Tests the retrieving of the baseurl for skolemization."""
    if Skolemizer.baseurl_key in os.environ.keys():
        del os.environ[Skolemizer.baseurl_key]

    assert Skolemizer.get_baseurl() == Skolemizer.baseurl_default_value

    os.environ[Skolemizer.baseurl_key] = Skolemizer.baseurl_default_value

    assert Skolemizer.baseurl_key in os.environ
    assert os.environ[Skolemizer.baseurl_key] == Skolemizer.baseurl_default_value


def test_get_baseurl_not_valid_url() -> None:
    """Tests the retrieving of the baseurl for skolemization."""
    if Skolemizer.baseurl_key in os.environ.keys():
        del os.environ[Skolemizer.baseurl_key]

    os.environ[Skolemizer.baseurl_key] = Skolemizer.baseurl_default_value + "<>"

    assert Skolemizer.get_baseurl() == Skolemizer.baseurl_default_value


def test_get_baseurl_missing_slash_at_end() -> None:
    """Tests the retrieving of the baseurl for skolemization."""
    if Skolemizer.baseurl_key in os.environ.keys():
        del os.environ[Skolemizer.baseurl_key]

    os.environ[Skolemizer.baseurl_key] = Skolemizer.baseurl_default_value[:-1]

    assert Skolemizer.get_baseurl() == Skolemizer.baseurl_default_value


def test_has_skolemization_morfologi_invalid_url() -> None:
    """Tests skolemization for invalid url."""
    skolemization = Skolemizer.add_skolemization()

    assert skolemization.startswith(
        Skolemizer.baseurl_default_value + ".well-known/skolem/"
    )

    assert Skolemizer.has_skolemization_morfologi(skolemization)
    assert not Skolemizer.has_skolemization_morfologi(skolemization + "<")
