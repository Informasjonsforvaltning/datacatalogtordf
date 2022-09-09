"""Contact module for mapping a datacatalog to rdf.

This module contains methods for mapping a contact object to rdf
according to the
`vcard ontology <https://www.w3.org/2006/vcard/ns-2006.html>`__

Example:
    >>> from datacatalogtordf import Contact
    >>>
    >>> contact = Contact()
    >>> contact.identifier = "http://example.com/contacts/1"
    >>> contact.name = {'nb': 'Digitaliseringsdirektoratet'}
    >>> bool(contact.to_rdf())
    True
"""
from __future__ import annotations

from typing import Dict, Optional

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from skolemizer import Skolemizer  # type: ignore

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class Contact:
    """A class representing a vcard:Contact.

    Attributes:
        identifier: unique uri for contact
        name: name of contact in various languages
        email: email as a mailto link
        telephone: telephone number
        url: url to website
    """

    _identifier: str
    _name: dict
    _email: str
    _telephone: str
    _url: str

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self._identifier = identifier

        self._g = Graph()

    @property
    def identifier(self) -> str:
        """Identifier attribute.

        Returns:
            a string holding a valid uri
        """
        return self._identifier

    @identifier.setter
    def identifier(self, uri: str) -> None:
        self._identifier = uri

    @property
    def name(self) -> dict:
        """Get/set for name."""
        return self._name

    @name.setter
    def name(self, name: dict) -> None:
        self._name = name

    @property
    def email(self) -> str:
        """Get/set for email."""
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        self._email = email

    @property
    def telephone(self) -> str:
        """Get/set for telephone."""
        return self._telephone

    @telephone.setter
    def telephone(self, telephone: str) -> None:
        self._telephone = telephone

    @property
    def url(self) -> str:
        """Get/set for url."""
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        self._url = url

    def to_json(self) -> Dict:
        """Convert the Contact to a json / dict. It will omit the non-initalized fields.

        Returns:
            Dict: The json representation of this instance.
        """
        output = {"_type": type(self).__name__}
        # Add ins for optional top level attributes
        for k in dir(self):
            try:
                v = getattr(self, k)
                is_method = callable(v)
                is_private = k.startswith("_")
                if is_method or is_private:
                    continue

                to_json = hasattr(v, "to_json") and callable(getattr(v, "to_json"))
                output[k] = v.to_json() if to_json else v

            except AttributeError:
                continue

        return output

    @classmethod
    def from_json(cls, json: Dict) -> Contact:
        """Convert a JSON (dict).

        Args:
            json: A dict representing this class.

        Returns:
            Contact: The object.
        """
        resource = cls()
        for key in json:
            is_private = key.startswith("_")
            if not is_private:
                setattr(resource, key, json[key])

        return resource

    def _to_graph(self) -> Graph:

        self._add_contact_to_graph()

        return self._g

    def to_rdf(self, format: str = "text/turtle") -> str:
        """Maps the contact to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format: a valid format.

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format)

    # -----

    def _add_contact_to_graph(self: Contact) -> None:
        """Adds the concept to the Graph _g."""
        self._g.bind("vcard", VCARD)

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)
        self._g.add((_self, RDF.type, VCARD.Organization))

        # name
        if getattr(self, "name", None):
            for key in self.name:
                self._g.add(
                    (
                        _self,
                        VCARD.hasOrganizationName,
                        Literal(self.name[key], lang=key),
                    )
                )

        # email
        if getattr(self, "email", None):
            self._g.add((_self, VCARD.hasEmail, URIRef("mailto:" + self.email)))

        # telephone
        if getattr(self, "telephone", None):
            self._g.add((_self, VCARD.hasTelephone, URIRef("tel:" + self.telephone)))

        # url
        if getattr(self, "url", None):
            self._g.add((_self, VCARD.hasURL, URIRef(self.url)))
