"""Catalog module for mapping a catalog to rdf.

This module contains methods for mapping a catalog object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-katalog>`__

Example:
    >>> from datacatalogtordf import Catalog, Dataset
    >>>
    >>> catalog = Catalog()
    >>> catalog.identifier = "http://example.com/catalogs/1"
    >>> catalog.title = {"en": "Title of catalog"}
    >>>
    >>> a_dataset = Dataset()
    >>> a_dataset.identifier = "http://example.com/datasets/1"
    >>> catalog.datasets.append(a_dataset)
    >>>
    >>> bool(catalog.to_rdf())
    True

"""
from __future__ import annotations

from typing import List

from rdflib import Graph, Namespace, RDF, URIRef

from .dataset import Dataset
from .uri import URI


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class Catalog(Dataset):
    """A class representing a dcat:Catalog.

    Ref: `dcat:Catalog <https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog>`_.

    Attributes:
        datasets: list of datsets in catalog
        homepage: link to a homepage for the catalog
    """

    __slots__ = ("_datasets", "_homepage")
    _datasets: List
    _homepage: str

    def __init__(self) -> None:
        """Inits catalog object with default values."""
        super().__init__()
        self._type = DCAT.Catalog
        self.datasets = []

    @property
    def datasets(self: Catalog) -> List[Dataset]:
        """Get/set for datasets."""
        return self._datasets

    @datasets.setter
    def datasets(self: Catalog, datasets: List[Dataset]) -> None:
        self._datasets = datasets

    @property
    def homepage(self: Catalog) -> str:
        """Get/set for homepage."""
        return self._homepage

    @homepage.setter
    def homepage(self: Catalog, homepage: str) -> None:
        self._homepage = URI(homepage)

    # -
    def _to_graph(self: Catalog) -> Graph:

        super(Catalog, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._datasets_to_graph()
        self._homepage_to_graph()

        return self._g

    def _datasets_to_graph(self: Catalog) -> None:

        if getattr(self, "datasets", None):
            for dataset in self._datasets:
                self._g.add(
                    (URIRef(self.identifier), DCAT.dataset, URIRef(dataset.identifier))
                )

    def _homepage_to_graph(self: Catalog) -> None:

        if getattr(self, "homepage", None):
            self._g.add((URIRef(self.identifier), FOAF.homepage, URIRef(self.homepage)))
