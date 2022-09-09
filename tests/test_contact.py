"""Test cases for the contact module."""
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization

from datacatalogtordf import Contact
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns a identifier graph isomorphic to spec."""
    contact = Contact("http://example.com/contact/1")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix ns1: <http://www.w3.org/2006/vcard/ns#> .

    <http://example.com/contact/1> a ns1:Organization .
    """
    g1 = Graph().parse(data=contact.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a contact graph as with skolemization node isomorphic to spec."""
    contact = Contact()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix ns1: <http://www.w3.org/2006/vcard/ns#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a ns1:Organization  .

        """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=contact.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_name_as_graph() -> None:
    """It returns a title graph isomorphic to spec."""
    contact = Contact()
    contact.identifier = "http://example.com/contacts/1"
    contact.name = {"en": "James Bond", "nb": "Djeims Bånd"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix ns1: <http://www.w3.org/2006/vcard/ns#> .
    <http://example.com/contacts/1> a ns1:Organization ;
        ns1:hasOrganizationName "James Bond"@en, "Djeims Bånd"@nb ;
        .
    """
    g1 = Graph().parse(data=contact.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_email_as_graph() -> None:
    """It returns a contact graph isomorphic to spec."""
    """It returns an name graph isomorphic to spec."""
    contact = Contact()
    contact.identifier = "http://example.com/contacts/1"
    contact.email = "james.bond@mi6.com"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix ns1: <http://www.w3.org/2006/vcard/ns#> .
    <http://example.com/contacts/1> a ns1:Organization ;
        ns1:hasEmail <mailto:james.bond@mi6.com>
        .
        """
    g1 = Graph().parse(data=contact.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_telephone_as_graph() -> None:
    """It returns a contact graph isomorphic to spec."""
    """It returns an name graph isomorphic to spec."""
    contact = Contact()
    contact.identifier = "http://example.com/contacts/1"
    contact.telephone = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix ns1: <http://www.w3.org/2006/vcard/ns#> .
    <http://example.com/contacts/1> a ns1:Organization ;
        ns1:hasTelephone <tel:123456789>
        .
        """
    g1 = Graph().parse(data=contact.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_url_as_graph() -> None:
    """It returns a contact graph isomorphic to spec."""
    """It returns an name graph isomorphic to spec."""
    contact = Contact()
    contact.identifier = "http://example.com/contacts/1"
    contact.url = "http://contact-url"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix ns1: <http://www.w3.org/2006/vcard/ns#> .
    <http://example.com/contacts/1> a ns1:Organization ;
        ns1:hasURL <http://contact-url>
        .
        """
    g1 = Graph().parse(data=contact.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_json_should_return_contact_as_json_dict() -> None:
    """It returns a contact json dict."""
    contact = Contact()
    contact.identifier = "http://example.com/contact/1"
    contact.name = {"nb": "Contact A", "en": "Contact A"}

    json = contact.to_json()

    assert json == {
        "_type": "Contact",
        "identifier": "http://example.com/contact/1",
        "name": {"nb": "Contact A", "en": "Contact A"},
    }


def test_from_json_should_return_contact() -> None:
    """It returns a contact instance."""
    contact = Contact()
    contact.identifier = "http://example.com/contact/1"
    contact.name = {"nb": "Contact A", "en": "Contact A"}
    contact.email = "john.doe@email.com"
    contact.telephone = "123456789"
    contact.url = "http://contact-url"

    json = contact.to_json()

    contact_from_json = Contact.from_json(json)

    g1 = Graph().parse(data=contact.to_rdf(), format="turtle")
    g2 = Graph().parse(data=contact_from_json.to_rdf(), format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Utils for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="turtle").splitlines():
        if _l:
            print(_l)
