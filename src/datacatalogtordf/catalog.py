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

from typing import Any, List, Optional

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from .catalogrecord import CatalogRecord
from .dataservice import DataService
from .dataset import Dataset
from .resource import Resource
from .uri import URI


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")


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
        models (List[URI]): A list of links to InformationModels
    """

    __slots__ = (
        "_homepage",
        "_themes",
        "_has_parts",
        "_datasets",
        "_services",
        "_catalogs",
        "_catalogrecords",
        "_models",
        "_dct_identifier",
    )

    _homepage: URI
    _themes: List[str]
    _has_parts: List[Resource]
    _datasets: List[Dataset]
    _services: List[DataService]
    _catalogs: List[Catalog]
    _catalogrecords: List[CatalogRecord]
    _models: List[Any]
    _dct_identifier: str

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
        self.models = []

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
    def models(self: Catalog) -> List[Any]:
        """Get/set for models."""
        return self._models

    @models.setter
    def models(self: Catalog, models: List[Any]) -> None:
        self._models = models

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

    @property
    def dct_identifier(self) -> str:
        """Get for dct_identifier."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self, dct_identifier: str) -> None:
        """Set for dct_identifier."""
        self._dct_identifier = dct_identifier

        # -

    def to_rdf(
        self: Catalog,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
        include_datasets: bool = True,
        include_services: bool = True,
        include_models: bool = True,
    ) -> bytes:
        """Maps the catalog to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format (str): a valid format.
            encoding (str): the encoding to serialize into
            include_datasets (bool): includes the dataset graphs in the catalog
            include_services (bool): includes the services in the catalog
            include_models (bool): includes the models in the catalog

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph(
            include_datasets, include_services, include_models
        ).serialize(format=format, encoding=encoding)

    # -

    def _to_graph(
        self: Catalog,
        include_datasets: bool = True,
        include_services: bool = True,
        include_models: bool = True,
    ) -> Graph:
        super(Catalog, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._dct_identifier_to_graph()
        self._homepage_to_graph()
        self._themes_to_graph()
        self._has_parts_to_graph()
        self._datasets_to_graph()
        self._services_to_graph()
        self._catalogs_to_graph()
        self._catalogrecords_to_graph()
        self._models_to_graph()

        # Add all the datasets to the graf
        if include_datasets:
            for dataset in self._datasets:
                self._g += dataset._to_graph()

        # Add all the services to the graf
        if include_services:
            for service in self._services:
                self._g += service._to_graph()

        # Add all the models to the graf
        if include_models:
            for model in self._models:
                self._g += model._to_graph()

        return self._g

    def _dct_identifier_to_graph(self: Dataset) -> None:
        if getattr(self, "dct_identifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.identifier,
                    Literal(self.dct_identifier),
                )
            )

    def _homepage_to_graph(self: Catalog) -> None:
        if getattr(self, "homepage", None):
            self._g.add((URIRef(self.identifier), FOAF.homepage, URIRef(self.homepage)))

    def _themes_to_graph(self: Catalog) -> None:
        if getattr(self, "themes", None):
            for _theme in self._themes:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.themeTaxonomy,
                        URIRef(_theme),
                    )
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

    def _models_to_graph(self: Catalog) -> None:
        if getattr(self, "models", None):
            for _model in self._models:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        MODELLDCATNO.model,
                        URIRef(_model.identifier),
                    )
                )
