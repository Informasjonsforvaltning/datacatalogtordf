"""DatasetSeries module for mapping a dataset_series to rdf.

This module contains methods for mapping a dataset_series object to rdf
according to the
`dcat-ap-no v.2 standard <https://informasjonsforvaltning.github.io/dcat-ap-no/#klasse-datasettSerie>`__

Example:
    >>> from datacatalogtordf import Catalog, DatasetSeries, Dataset
    >>>
    >>> dataset_series = DatasetSeries("http://example.com/dataset_series/1")
    >>> dataset_series.title = {"en": "Title of dataset_series"}
    >>>
    >>> catalog = Catalog("http://example.com/catalog/1")
    >>> catalog.datasets.append(dataset_series)
    >>>
    >>> first_dataset = Dataset()
    >>> first_dataset.identifier = "http://example.com/datasets/1"
    >>> first_dataset.in_series = dataset_series
    >>>
    >>> second_dataset = Dataset()
    >>> second_dataset.identifier = "http://example.com/datasets/2"
    >>> second_dataset.in_series = dataset_series
    >>> second_dataset.prev = first_dataset
    >>>
    >>> dataset_series.first = first_dataset
    >>> dataset_series.last = second_dataset
    >>>
    >>> bool(catalog.to_rdf())
    True

"""
from __future__ import annotations

from typing import Optional, Union

from rdflib import Graph, Namespace, URIRef

from .dataset import Dataset


DCAT = Namespace("http://www.w3.org/ns/dcat#")


class DatasetSeries(Dataset):
    """A class representing a dcat:DatasetSeries.

    Ref: `dcat:DatasetSeries <https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset_Series>`_.

    Args:
        identifier (URI): the identifier of the dataset-series.
    """

    __slots__ = (
        "_first",
        "_last",
    )

    # Types
    _first: Dataset  # 6.4.31
    _last: Dataset  # 6.4.32

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits dataset_series object with default values."""
        super().__init__()

        if identifier:
            self.identifier = identifier

        self._type = DCAT.DatasetSeries

    # -

    @property
    def first(self: DatasetSeries) -> Dataset:
        """Dataset: The first resource in an ordered collection or series of resources, to which the current resource belongs."""  # noqa: B950
        return self._first

    @first.setter
    def first(self: DatasetSeries, first: Dataset) -> None:
        self._first = first

    @property
    def last(self: DatasetSeries) -> Dataset:
        """Dataset: The last resource in an ordered collection or series of resources, to which the current resource belongs."""  # noqa: B950
        return self._last

    @last.setter
    def last(self: DatasetSeries, last: Dataset) -> None:
        self._last = last

    # -

    def to_rdf(
        self: DatasetSeries,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
        include_datasets: bool = True,
        include_services: bool = True,
        include_models: bool = True,
        include_contains_services: bool = True,
    ) -> Union[bytes, str]:
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
            include_contains_services (bool): includes the services (cpsvno) in the catalog

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph(
            include_datasets,
            include_services,
            include_models,
            include_contains_services,
        ).serialize(format=format, encoding=encoding)

    # -

    def _to_graph(
        self: DatasetSeries,
        include_datasets: bool = True,
        include_services: bool = True,
        include_models: bool = True,
        include_contains_services: bool = True,
    ) -> Graph:

        super(DatasetSeries, self)._to_graph()

        self._first_to_graph()
        self._last_to_graph()

        # Add all the datasets in the series to the graf based on last/prev:
        if include_datasets:
            if self.last:
                self._g += self.last._to_graph()
                _prev = self.last.prev
                while True:
                    self._g += _prev._to_graph()
                    if getattr(_prev, "prev", None):
                        _prev = _prev.prev
                    else:
                        break  # pragma: no cover

        return self._g

    def _first_to_graph(self: DatasetSeries) -> None:
        if getattr(self, "first", None):
            self._g.add(
                (URIRef(self.identifier), DCAT.first, URIRef(self.first.identifier))
            )

    def _last_to_graph(self: DatasetSeries) -> None:
        if getattr(self, "last", None):
            self._g.add(
                (URIRef(self.identifier), DCAT.last, URIRef(self.last.identifier))
            )
