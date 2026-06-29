"""Test cases for the skolemizer module."""

import pytest

from datacatalogtordf.skolemizer import Skolemizer


@pytest.fixture(autouse=True)
def reset_skolemizer_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reset skolemizer state between tests."""
    Skolemizer.skolemizations.clear()
    monkeypatch.delenv(Skolemizer.baseurl_key, raising=False)


def test_is_exact_skolemization_returns_true_for_known_uri() -> None:
    """It returns True when the URI was created by add_skolemization."""
    skolem_uri = Skolemizer.add_skolemization()

    assert Skolemizer.is_exact_skolemization(skolem_uri) is True


def test_has_skolemization_morfologi_returns_false_for_invalid_uri() -> None:
    """It returns False when the URI contains invalid characters."""
    assert (
        Skolemizer.has_skolemization_morfologi("http://example.com/invalid uri")
        is False
    )


def test_has_skolemization_morfologi_returns_true_for_valid_form() -> None:
    """It returns True when the URI matches the skolemization pattern."""
    skolem_uri = (
        Skolemizer.get_baseurl()
        + ".well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94"
    )

    assert Skolemizer.has_skolemization_morfologi(skolem_uri) is True


def test_get_baseurl_falls_back_to_default_for_invalid_env_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It uses the default baseurl when the environment value is invalid."""
    monkeypatch.setenv(Skolemizer.baseurl_key, "http://example.com/invalid path")

    assert Skolemizer.get_baseurl() == Skolemizer.baseurl_default_value


def test_get_baseurl_appends_trailing_slash(monkeypatch: pytest.MonkeyPatch) -> None:
    """It ensures the baseurl ends with a trailing slash."""
    monkeypatch.setenv(Skolemizer.baseurl_key, "http://example.org")

    assert Skolemizer.get_baseurl() == "http://example.org/"


def test_is_valid_uri_returns_true_for_valid_uri() -> None:
    """It returns True when the URI contains no invalid characters."""
    assert Skolemizer._is_valid_uri("http://example.com/valid-uri") is True
