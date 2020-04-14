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
from .periodoftime import PeriodOfTime
from .resource import Resource
from .uri import URI

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
PROV = Namespace("http://www.w3.org/ns/prov#")
DCATNO = Namespace("https://data.norge.no/vocabulary/dcatno#")


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
        "_period_of_time",
        "_temporal_resolution",
        "_was_generated_by",
        "_access_rights_comments",
    )

    # Types
    _distributions: List[Distribution]
    _frequency: URI
    _spatial_coverage: Location
    _spatial_resolution: Decimal
    _period_of_time: PeriodOfTime
    _temporal_resolution: str
    _was_generated_by: URI
    _access_rights_comments: List[URI]

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()
        self._type = DCAT.Dataset
        self.distributions = []
        self.access_rights_comments = []
        self._g.bind("dcatno", DCATNO)

    @property
    def distributions(self: Dataset) -> List[Distribution]:
        """Get/set for distributions."""
        return self._distributions

    @distributions.setter
    def distributions(self: Dataset, distributions: List[Distribution]) -> None:
        self._distributions = distributions

    @property
    def frequency(self: Dataset) -> URI:
        """Get/set for frequency."""
        return self._frequency

    @frequency.setter
    def frequency(self: Dataset, frequency: URI) -> None:
        self._frequency = frequency

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

    @property
    def period_of_time(self: Dataset) -> PeriodOfTime:
        """Get/set for period_of_time."""
        return self._period_of_time

    @period_of_time.setter
    def period_of_time(self: Dataset, period_of_time: PeriodOfTime) -> None:
        self._period_of_time = period_of_time

    @property
    def temporal_resolution(self: Dataset) -> str:
        """Get/set for temporal_resolution."""
        return self._temporal_resolution

    @temporal_resolution.setter
    def temporal_resolution(self: Dataset, temporal_resolution: str) -> None:
        self._temporal_resolution = temporal_resolution

    @property
    def was_generated_by(self: Dataset) -> URI:
        """Get/set for was_generated_by."""
        return self._was_generated_by

    @was_generated_by.setter
    def was_generated_by(self: Dataset, was_generated_by: URI) -> None:
        self._was_generated_by = was_generated_by

    @property
    def access_rights_comments(self: Dataset) -> List[URI]:
        """Get/set for access_rights_comments."""
        return self._access_rights_comments

    @access_rights_comments.setter
    def access_rights_comments(
        self: Dataset, access_rights_comments: List[URI]
    ) -> None:
        self._access_rights_comments = access_rights_comments

    # -
    def _to_graph(self: Dataset) -> Graph:

        super(Dataset, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._distributions_to_graph()
        self._frequency_to_graph()
        self._spatial_coverage_to_graph()
        self._spatial_resolution_to_graph()
        self._period_of_time_to_graph()
        self._temporal_resolution_to_graph()
        self._was_generated_by_to_graph()
        self._access_rights_comments_to_graph()

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
            for _s, p, o in self.spatial_coverage._to_graph().triples(
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

    def _period_of_time_to_graph(self: Dataset) -> None:
        if getattr(self, "period_of_time", None):
            _temporal = BNode()
            for _s, p, o in self.period_of_time._to_graph().triples((None, None, None)):
                self._g.add((_temporal, p, o))
            self._g.add((URIRef(self.identifier), DCT.temporal, _temporal,))

    def _temporal_resolution_to_graph(self: Dataset) -> None:
        if getattr(self, "temporal_resolution", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.temporalResolution,
                    Literal(self.temporal_resolution, datatype=XSD.duration),
                )
            )

    def _was_generated_by_to_graph(self: Dataset) -> None:
        if getattr(self, "was_generated_by", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    PROV.wasGeneratedBy,
                    URIRef(self.was_generated_by),
                )
            )

    def _access_rights_comments_to_graph(self: Dataset) -> None:
        if getattr(self, "access_rights_comments", None):
            for _access_rights_comment in self._access_rights_comments:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCATNO.accessRightsComment,
                        URIRef(_access_rights_comment),
                    )
                )
