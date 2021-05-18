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
from typing import List, Optional, Union

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
        distributions (List[Distribution]): A list of distributions of the dataset
        frequency (URI): A link to resource describing the frequency at\
            which dataset is published.
        spatial_coverage (Location): The geographical area covered by the dataset.
        spatial_resolution (Decimal): Minimum spatial separation resolvable \
            in a dataset, measured in meters.
        temporal_coverage (PeriodOfTime): The temporal period that the dataset covers.
        temporal_resolution (str): Minimum time period resolvable in the dataset.
        was_generated_by (URI): A link to an activity that generated, \
            or provides the business context for, the creation of the dataset.
        access_rights_comments (List[URI]): Referanse til hjemmel \
            (kilde for påstand) i offentlighetsloven, sikkerhetsloven, \
            beskyttelsesinstruksen eller annet lovverk som ligger til grunn for \
            vurdering av tilgangsnivå.
    """

    __slots__ = (
        "_distributions",
        "_type",
        "_frequency",
        "_spatial_coverage",
        "_spatial_resolution",
        "_temporal_coverage",
        "_temporal_resolution",
        "_was_generated_by",
        "_access_rights_comments",
        "_dct_identifier",
    )

    # Types
    _distributions: List[Distribution]
    _frequency: URI
    _spatial_coverage: Union[Location, str]
    _spatial_resolution: Decimal
    _temporal_coverage: PeriodOfTime
    _temporal_resolution: str
    _was_generated_by: URI
    _access_rights_comments: List[str]
    _dct_identifier: str

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()
        self._type = DCAT.Dataset
        self.distributions = []
        self.access_rights_comments = []

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
    def spatial_coverage(self: Dataset) -> Union[Location, str]:
        """Get/set for spatial_coverage."""
        return self._spatial_coverage

    @spatial_coverage.setter
    def spatial_coverage(self: Dataset, spatial_coverage: Union[Location, str]) -> None:
        self._spatial_coverage = spatial_coverage

    @property
    def spatial_resolution(self: Dataset) -> Decimal:
        """Get/set for spatial_resolution."""
        return self._spatial_resolution

    @spatial_resolution.setter
    def spatial_resolution(self: Dataset, spatial_resolution: Decimal) -> None:
        self._spatial_resolution = spatial_resolution

    @property
    def temporal_coverage(self: Dataset) -> PeriodOfTime:
        """Get/set for temporal_coverage."""
        return self._temporal_coverage

    @temporal_coverage.setter
    def temporal_coverage(self: Dataset, temporal_coverage: PeriodOfTime) -> None:
        self._temporal_coverage = temporal_coverage

    @property
    def temporal_resolution(self: Dataset) -> str:
        """Get/set for temporal_resolution."""
        return self._temporal_resolution

    @temporal_resolution.setter
    def temporal_resolution(self: Dataset, temporal_resolution: str) -> None:
        self._temporal_resolution = temporal_resolution

    @property
    def was_generated_by(self: Dataset) -> str:
        """Get/set for was_generated_by."""
        return self._was_generated_by

    @was_generated_by.setter
    def was_generated_by(self: Dataset, was_generated_by: str) -> None:
        self._was_generated_by = URI(was_generated_by)

    @property
    def access_rights_comments(self: Dataset) -> List[str]:
        """Get/set for access_rights_comments."""
        return self._access_rights_comments

    @access_rights_comments.setter
    def access_rights_comments(
        self: Dataset, access_rights_comments: List[str]
    ) -> None:
        self._access_rights_comments = access_rights_comments

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
        self: Dataset,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
        include_distributions: bool = True,
    ) -> bytes:
        """Maps the catalog to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format (str): a valid format.
            encoding (str): the encoding to serialize into
            include_distributions (bool): includes the distributions in the graph

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph(include_distributions).serialize(
            format=format, encoding=encoding
        )

    def _to_graph(
        self: Dataset,
        include_distributions: bool = True,
    ) -> Graph:

        super(Dataset, self)._to_graph()
        self._g.bind("dcatno", DCATNO)

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._dct_identifier_to_graph()
        self._distributions_to_graph()
        self._frequency_to_graph()
        self._spatial_coverage_to_graph()
        self._spatial_resolution_to_graph()
        self._temporal_coverage_to_graph()
        self._temporal_resolution_to_graph()
        self._was_generated_by_to_graph()
        self._access_rights_comments_to_graph()

        # Add all the distributions to the graf
        if include_distributions:
            for distribution in self._distributions:
                self._g += distribution._to_graph()

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
            if isinstance(self.spatial_coverage, Location):

                if not getattr(self.spatial_coverage, "identifier", None):
                    _location = BNode()
                else:
                    _location = URIRef(self.spatial_coverage.identifier)  # type: ignore

                for _s, p, o in self.spatial_coverage._to_graph().triples(  # type: ignore
                    (None, None, None)
                ):
                    self._g.add((_location, p, o))

            elif isinstance(self.spatial_coverage, str):
                _location = URIRef(self.spatial_coverage)

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

    def _temporal_coverage_to_graph(self: Dataset) -> None:
        if getattr(self, "temporal_coverage", None):
            _temporal = BNode()
            for _s, p, o in self.temporal_coverage._to_graph().triples(
                (None, None, None)
            ):
                self._g.add((_temporal, p, o))
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.temporal,
                    _temporal,
                )
            )

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
