"""Dataset module for mapping a dataset to rdf.

This module contains methods for mapping a dataset object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-dataset>`__

Example:
    >>> from datacatalogtordf import Dataset, Distribution
    >>>
    >>> dataset = Dataset()
    >>> dataset.identifier = "http://example.com/datasets/1"
    >>> dataset.title = {"en": "Title of dataset"}
    >>>
    >>> a_distribution = Distribution()
    >>> a_distribution.identifier = "http://example.com/dataservices/1"
    >>> a_distribution.title = {"en": "Title of distribution"}
    >>> dataset.distributions.append(a_distribution)
    >>>
    >>> bool(dataset.to_rdf())
    True
"""
from __future__ import annotations

from decimal import Decimal
from typing import List

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

from .distribution import Distribution
from .location import Location
from .resource import Resource
from .uri import URI

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


class Dataset(Resource):
    """A class representing a dcat:Dataset.

    Ref: `dcat:Dataset <https://www.w3.org/TR/vocab-dcat-2/#Class:Dataset>`_.

    Attributes:
        distributions: a list of distributions of the dataset
    """

    __slots__ = (
        "_distributions",
        "_type",
        "_frequency",
        "_spatial_coverage",
        "_spatial_resolution",
    )

    # Types
    _distributions: List
    _frequency: str
    _spatial_coverage: Location
    _spatial_resolution: Decimal

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()
        self._type = DCAT.Dataset
        self.distributions = []

    @property
    def distributions(self: Dataset) -> List[Distribution]:
        """Get/set for distributions."""
        return self._distributions

    @distributions.setter
    def distributions(self: Dataset, distributions: List[Distribution]) -> None:
        self._distributions = distributions

    @property
    def frequency(self: Dataset) -> str:
        """Get/set for frequency."""
        return self._frequency

    @frequency.setter
    def frequency(self: Dataset, frequency: str) -> None:
        self._frequency = URI(frequency)

    @property
    def spatial_coverage(self: Dataset) -> Location:
        """Get/set for spatial_coverage."""
        return self._spatial_coverage

    @spatial_coverage.setter
    def spatial_coverage(self: Dataset, spatial_coverage: Location) -> None:
        self._spatial_coverage = spatial_coverage

    @property
    def spatial_resolution(self: Dataset) -> Decimal:
        """Get/set for spatial_resolution."""
        return self._spatial_resolution

    @spatial_resolution.setter
    def spatial_resolution(self: Dataset, spatial_resolution: Decimal) -> None:
        self._spatial_resolution = spatial_resolution

    # -
    def _to_graph(self: Dataset) -> Graph:

        super(Dataset, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._distributions_to_graph()
        self._frequency_to_graph()
        self._spatial_coverage_to_graph()
        self._spatial_resolution_to_graph()

        return self._g

    def _distributions_to_graph(self: Dataset) -> None:
        if getattr(self, "distributions", None):
            for distribution in self._distributions:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.distribution,
                        URIRef(distribution.identifier),
                    )
                )

    def _frequency_to_graph(self: Dataset) -> None:
        if getattr(self, "frequency", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.accrualPeriodicity,
                    URIRef(self.frequency),
                )
            )

    def _spatial_coverage_to_graph(self: Dataset) -> None:
        if getattr(self, "spatial_coverage", None):
            _location = BNode()
            for _s, p, o in self._spatial_coverage._to_graph().triples(
                (None, None, None)
            ):
                self._g.add((_location, p, o))
            self._g.add((URIRef(self.identifier), DCT.spatial, _location))

    def _spatial_resolution_to_graph(self: Dataset) -> None:
        if getattr(self, "spatial_resolution", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.spatialResolutionInMeters,
                    Literal(self.spatial_resolution, datatype=XSD.decimal),
                )
            )
