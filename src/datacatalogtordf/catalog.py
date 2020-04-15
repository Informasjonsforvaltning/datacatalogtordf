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

from .catalogrecord import CatalogRecord
from .dataservice import DataService
from .dataset import Dataset
from .resource import Resource
from .uri import URI


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class Catalog(Dataset):
    """A class representing a dcat:Catalog.

    Ref: `dcat:Catalog <https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog>`_.

    Attributes:
        homepage (URI): A link to a homepage for the catalog
        themes (List[URI]): A list of links to knowledge organization system (KOS) \
                    used to classify catalog
        has_parts (List[Resource]): A list of resources that is listed in the catalog.
        datasets (List[Dataset]): A list of datasets that is listed in the catalog.
        services (List[DataService]): A list of dataservices of sites or \
                    end-points that is listed in the catalog.
        catalogs (List[Catalog]): A list of catalogs that are of interest in \
                    the context of this catalog.
        catalogrecords (List[CatalogRecord]): A list of records describing \
                    the registration of a single dataset or data service \
                    that is part of the catalog.
    """

    __slots__ = (
        "_homepage",
        "_themes",
        "_has_parts",
        "_datasets",
        "_services",
        "_catalogs",
        "_catalogrecords",
    )

    _homepage: URI
    _themes: List[str]
    _has_parts: List[Resource]
    _datasets: List[Dataset]
    _services: List[DataService]
    _catalogs: List[Catalog]
    _catalogrecords: List[CatalogRecord]

    def __init__(self) -> None:
        """Inits catalog object with default values."""
        super().__init__()
        self._type = DCAT.Catalog
        self.themes = []
        self.has_parts = []
        self.datasets = []
        self.services = []
        self.catalogs = []
        self.catalogrecords = []

    @property
    def homepage(self: Catalog) -> str:
        """Get/set for homepage."""
        return self._homepage

    @homepage.setter
    def homepage(self: Catalog, homepage: str) -> None:
        self._homepage = URI(homepage)

    @property
    def themes(self: Catalog) -> List[str]:
        """Get/set for themes."""
        return self._themes

    @themes.setter
    def themes(self: Catalog, themes: List[str]) -> None:
        self._themes = themes

    @property
    def has_parts(self: Catalog) -> List[Resource]:
        """Get/set for has_parts."""
        return self._has_parts

    @has_parts.setter
    def has_parts(self: Catalog, has_parts: List[Resource]) -> None:
        self._has_parts = has_parts

    @property
    def datasets(self: Catalog) -> List[Dataset]:
        """Get/set for datasets."""
        return self._datasets

    @datasets.setter
    def datasets(self: Catalog, datasets: List[Dataset]) -> None:
        self._datasets = datasets

    @property
    def services(self: Catalog) -> List[DataService]:
        """Get/set for services."""
        return self._services

    @services.setter
    def services(self: Catalog, services: List[DataService]) -> None:
        self._services = services

    @property
    def catalogs(self: Catalog) -> List[Catalog]:
        """Get/set for catalogs."""
        return self._catalogs

    @catalogs.setter
    def catalogs(self: Catalog, catalogs: List[Catalog]) -> None:
        self._catalogs = catalogs

    @property
    def catalogrecords(self: Catalog) -> List[CatalogRecord]:
        """Get/set for catalogrecords."""
        return self._catalogrecords

    @catalogrecords.setter
    def catalogrecords(self: Catalog, catalogrecords: List[CatalogRecord]) -> None:
        self._catalogrecords = catalogrecords

    # -
    def _to_graph(self: Catalog) -> Graph:

        super(Catalog, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._homepage_to_graph()
        self._themes_to_graph()
        self._has_parts_to_graph()
        self._datasets_to_graph()
        self._services_to_graph()
        self._catalogs_to_graph()
        self._catalogrecords_to_graph()

        return self._g

    def _homepage_to_graph(self: Catalog) -> None:
        if getattr(self, "homepage", None):
            self._g.add((URIRef(self.identifier), FOAF.homepage, URIRef(self.homepage)))

    def _themes_to_graph(self: Catalog) -> None:
        if getattr(self, "themes", None):
            for _theme in self._themes:
                self._g.add(
                    (URIRef(self.identifier), DCAT.themeTaxonomy, URIRef(_theme),)
                )

    def _has_parts_to_graph(self: Catalog) -> None:
        if getattr(self, "has_parts", None):
            for _resource in self._has_parts:
                self._g.add(
                    (URIRef(self.identifier), DCT.hasPart, URIRef(_resource.identifier))
                )

    def _datasets_to_graph(self: Catalog) -> None:
        if getattr(self, "datasets", None):
            for _dataset in self._datasets:
                self._g.add(
                    (URIRef(self.identifier), DCAT.dataset, URIRef(_dataset.identifier))
                )

    def _services_to_graph(self: Catalog) -> None:
        if getattr(self, "services", None):
            for _service in self._services:
                self._g.add(
                    (URIRef(self.identifier), DCAT.service, URIRef(_service.identifier))
                )

    def _catalogs_to_graph(self: Catalog) -> None:
        if getattr(self, "catalogs", None):
            for _catalog in self._catalogs:
                self._g.add(
                    (URIRef(self.identifier), DCAT.catalog, URIRef(_catalog.identifier))
                )

    def _catalogrecords_to_graph(self: Catalog) -> None:
        if getattr(self, "catalogrecords", None):
            for _catalogrecord in self._catalogrecords:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.record,
                        URIRef(_catalogrecord.identifier),
                    )
                )
