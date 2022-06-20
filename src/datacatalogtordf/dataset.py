"""Dataset module for mapping a dataset to rdf.

This module contains methods for mapping a dataset object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#klasse-dataset>`__

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
from typing import List, Optional, TYPE_CHECKING, Union

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef
from rdflib.term import Identifier
from skolemizer import Skolemizer

if TYPE_CHECKING:  # pragma: no cover
    from .dataset_series import DatasetSeries  # pytype: disable=pyi-error
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

    Args:
        identifier (URI): the identifier of the dataset.

    Ref: `dcat:Dataset <https://www.w3.org/TR/vocab-dcat-2/#Class:Dataset>`_.
    """

    __slots__ = (
        "_distributions",
        "_type",
        "_frequency",
        "_spatial",
        "_spatial_resolution_in_meters",
        "_temporal",
        "_temporal_resolution",
        "_was_generated_by",
        "_access_rights_comments",
        "_dct_identifier",
        "_in_series",
    )

    # Types
    _distributions: List[Distribution]
    _frequency: URI
    _spatial: List[Union[Location, str]]
    _spatial_resolution_in_meters: List[Decimal]
    _temporal: List[PeriodOfTime]
    _temporal_resolution: List[str]
    _was_generated_by: URI
    _access_rights_comments: List[str]
    _dct_identifier: str
    _in_series: DatasetSeries

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier

        super().__init__()
        self._type = DCAT.Dataset
        self.distributions = []
        self.access_rights_comments = []

    @property
    def distributions(self: Dataset) -> List[Distribution]:
        """List[Distribution]: A list of distributions of the dataset."""
        return self._distributions

    @distributions.setter
    def distributions(self: Dataset, distributions: List[Distribution]) -> None:
        self._distributions = distributions

    @property
    def frequency(self: Dataset) -> str:
        """[URI]: A link to resource describing the frequency at which dataset is published."""  # noqa: B950
        return self._frequency

    @frequency.setter
    def frequency(self: Dataset, frequency: str) -> None:
        self._frequency = URI(frequency)

    @property
    def spatial(self: Dataset) -> List[Union[Location, str]]:
        """List[Location]: A list of geographical areas covered by the dataset."""  # noqa: B950
        return self._spatial

    @spatial.setter
    def spatial(self: Dataset, spatial: List[Union[Location, str]]) -> None:
        self._spatial = spatial

    @property
    def spatial_resolution_in_meters(self: Dataset) -> List[Decimal]:
        """List[Decimal]: A list of minimum spatial separation resolvables in a dataset, measured in meters."""  # noqa: B950
        return self._spatial_resolution_in_meters

    @spatial_resolution_in_meters.setter
    def spatial_resolution_in_meters(
        self: Dataset, spatial_resolution_in_meters: List[Decimal]
    ) -> None:
        self._spatial_resolution_in_meters = spatial_resolution_in_meters

    @property
    def temporal(self: Dataset) -> List[PeriodOfTime]:
        """List[PeriodOfTime]: A list of temporal periods that the dataset covers."""  # noqa: B950
        return self._temporal

    @temporal.setter
    def temporal(self: Dataset, temporal: List[PeriodOfTime]) -> None:
        self._temporal = temporal

    @property
    def temporal_resolution(self: Dataset) -> List[str]:
        """List[str]: A list of minimum time period resolvables in the dataset."""  # noqa: B950
        return self._temporal_resolution

    @temporal_resolution.setter
    def temporal_resolution(self: Dataset, temporal_resolution: List[str]) -> None:
        self._temporal_resolution = temporal_resolution

    @property
    def was_generated_by(self: Dataset) -> str:
        """URI: A link to an activity that generated, or provides the business context for, the creation of the dataset."""  # noqa: B950
        return self._was_generated_by

    @was_generated_by.setter
    def was_generated_by(self: Dataset, was_generated_by: str) -> None:
        self._was_generated_by = URI(was_generated_by)

    @property
    def access_rights_comments(self: Dataset) -> List[str]:
        """List[URI]: Referanse til hjemmel (kilde for påstand) i offentlighetsloven, sikkerhetsloven, beskyttelsesinstruksen eller annet lovverk som ligger til grunn for vurdering av tilgangsnivå."""  # noqa: B950
        return self._access_rights_comments

    @access_rights_comments.setter
    def access_rights_comments(
        self: Dataset, access_rights_comments: List[str]
    ) -> None:
        self._access_rights_comments = access_rights_comments

    @property
    def dct_identifier(self) -> str:
        """str: the identifier for the dataset."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def in_series(self: Dataset) -> DatasetSeries:
        """DatasetSeries]: A dataset series of which the dataset is part."""
        return self._in_series

    @in_series.setter
    def in_series(self: Dataset, in_series: DatasetSeries) -> None:
        self._in_series = in_series

    # -
    def to_rdf(
        self: Dataset,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
        include_distributions: bool = True,
    ) -> Union[bytes, str]:
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

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        super(Dataset, self)._to_graph()
        self._g.bind("dcatno", DCATNO)

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._dct_identifier_to_graph()
        self._distributions_to_graph()
        self._frequency_to_graph()
        self._spatial_to_graph()
        self._spatial_resolution_in_meters_to_graph()
        self._temporal_to_graph()
        self._temporal_resolution_to_graph()
        self._was_generated_by_to_graph()
        self._access_rights_comments_to_graph()
        self._in_series_to_graph()

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

                if not getattr(distribution, "identifier", None):
                    distribution.identifier = Skolemizer.add_skolemization()

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

    def _spatial_to_graph(self: Dataset) -> None:
        if getattr(self, "spatial", None):
            for spatial in self.spatial:
                _location: Union[Identifier, None] = None
                if isinstance(spatial, Location):

                    if not getattr(spatial, "identifier", None):
                        _location = BNode()
                    else:
                        _location = URIRef(spatial.identifier)  # type: ignore

                    for _s, p, o in spatial._to_graph().triples(  # type: ignore
                        (None, None, None)
                    ):
                        self._g.add((_location, p, o))

                elif isinstance(spatial, str):
                    _location = URIRef(spatial)

                if _location is not None:
                    self._g.add((URIRef(self.identifier), DCT.spatial, _location))

    def _spatial_resolution_in_meters_to_graph(self: Dataset) -> None:
        if getattr(self, "spatial_resolution_in_meters", None):
            for resolution in self.spatial_resolution_in_meters:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.spatialResolutionInMeters,
                        Literal(resolution, datatype=XSD.decimal),
                    )
                )

    def _temporal_to_graph(self: Dataset) -> None:
        if getattr(self, "temporal", None):
            for temporal in self.temporal:
                _temporal = BNode()
                for _s, p, o in temporal._to_graph().triples((None, None, None)):
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
            for temporal_resolution in self.temporal_resolution:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.temporalResolution,
                        Literal(temporal_resolution, datatype=XSD.duration),
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

    def _in_series_to_graph(self: Dataset) -> None:
        if getattr(self, "in_series", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.inSeries,
                    URIRef(self.in_series.identifier),
                )
            )
