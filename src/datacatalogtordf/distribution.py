"""Distribution module for mapping a distribution to rdf.

This module contains methods for mapping a distribution object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-distribusjon>`__

Example:
    >>> from datacatalogtordf import Distribution
    >>>
    >>> distribution = Distribution()
    >>> distribution.identifier = "http://example.com/dataservices/1"
    >>> distribution.title = {"en": "Title of distribution"}
    >>>
    >>> bool(distribution.to_rdf())
    True
"""
from __future__ import annotations

from decimal import Decimal
from typing import List, TYPE_CHECKING

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS

from .periodoftime import Date
from .uri import URI

if TYPE_CHECKING:  # pragma: no cover
    from .dataservice import DataService  # pytype: disable=pyi-error

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")


class Distribution:
    """A class representing a dcat:Distribution.

    Ref: `dcat:Distribution <https://www.w3.org/TR/vocab-dcat-2/#Class:Distribution>`_

    Attributes:
        identifier: an URI uniquely identifying the resource
        title: a dict with title in multiple languages
    """

    __slots__ = (
        "_g",
        "_identifier",
        "_title",
        "_description",
        "_release_date",
        "_modification_date",
        "_license",
        "_access_rights",
        "_rights",
        "_has_policy",
        "_access_URL",
        "_access_service",
        "_download_URL",
        "_byte_size",
        "_spatial_resolution",
        "_temporal_resolution",
        "_conforms_to",
        "_media_types",
        "_formats",
        "_compression_format",
        "_package_format",
    )

    _identifier: str
    _title: dict
    _description: dict
    _release_date: str
    _modification_date: str
    _license: str
    _access_rights: str
    _rights: str
    _has_policy: str
    _access_URL: str
    _access_service: DataService
    _download_URL: str
    _byte_size: Decimal
    _spatial_resolution: Decimal
    _temporal_resolution: str
    _conforms_to: List[str]
    _media_types: List[str]
    _formats: List[str]
    _compression_format: str
    _package_format: str

    def __init__(self) -> None:
        """Inits an object with default values."""
        self.conforms_to = []
        self.media_types = []
        self.formats = []
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("xsd", XSD)

    @property
    def identifier(self: Distribution) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: Distribution, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def title(self: Distribution) -> dict:
        """Get/set for title."""
        return self._title

    @title.setter
    def title(self: Distribution, title: dict) -> None:
        self._title = title

    @property
    def description(self: Distribution) -> dict:
        """Description attribute."""
        return self._description

    @description.setter
    def description(self: Distribution, description: dict) -> None:
        self._description = description

    @property
    def release_date(self: Distribution) -> str:
        """Get/set for release_date."""
        return self._release_date

    @release_date.setter
    def release_date(self: Distribution, release_date: str) -> None:
        self._release_date = Date(release_date)

    @property
    def modification_date(self: Distribution) -> str:
        """Get/set for modification_date."""
        return self._modification_date

    @modification_date.setter
    def modification_date(self: Distribution, modification_date: str) -> None:
        self._modification_date = Date(modification_date)

    @property
    def license(self: Distribution) -> str:
        """Get/set for license."""
        return self._license

    @license.setter
    def license(self: Distribution, license: str) -> None:
        self._license = URI(license)

    @property
    def access_rights(self: Distribution) -> str:
        """Get/set for access_rights."""
        return self._access_rights

    @access_rights.setter
    def access_rights(self: Distribution, access_rights: str) -> None:
        self._access_rights = URI(access_rights)

    @property
    def rights(self: Distribution) -> str:
        """Get/set for rights."""
        return self._rights

    @rights.setter
    def rights(self: Distribution, rights: str) -> None:
        self._rights = URI(rights)

    @property
    def has_policy(self: Distribution) -> str:
        """Get/set for has_policy."""
        return self._has_policy

    @has_policy.setter
    def has_policy(self: Distribution, has_policy: str) -> None:
        self._has_policy = URI(has_policy)

    @property
    def access_URL(self: Distribution) -> str:
        """Get/set for access_URL."""
        return self._access_URL

    @access_URL.setter
    def access_URL(self: Distribution, access_URL: str) -> None:
        self._access_URL = URI(access_URL)

    @property
    def access_service(self: Distribution) -> DataService:
        """Get/set for access_service."""
        return self._access_service

    @access_service.setter
    def access_service(self: Distribution, access_service: DataService) -> None:
        self._access_service = access_service

    @property
    def download_URL(self: Distribution) -> str:
        """Get/set for download_URL."""
        return self._download_URL

    @download_URL.setter
    def download_URL(self: Distribution, download_URL: str) -> None:
        self._download_URL = URI(download_URL)

    @property
    def byte_size(self: Distribution) -> Decimal:
        """Get/set for byte_size."""
        return self._byte_size

    @byte_size.setter
    def byte_size(self: Distribution, byte_size: Decimal) -> None:
        self._byte_size = byte_size

    @property
    def spatial_resolution(self: Distribution) -> Decimal:
        """Get/set for spatial_resolution."""
        return self._spatial_resolution

    @spatial_resolution.setter
    def spatial_resolution(self: Distribution, spatial_resolution: Decimal) -> None:
        self._spatial_resolution = spatial_resolution

    @property
    def temporal_resolution(self: Distribution) -> str:
        """Get/set for temporal_resolution."""
        return self._temporal_resolution

    @temporal_resolution.setter
    def temporal_resolution(self: Distribution, temporal_resolution: str) -> None:
        self._temporal_resolution = temporal_resolution

    @property
    def conforms_to(self: Distribution) -> List[str]:
        """Get/set for conforms_to."""
        return self._conforms_to

    @conforms_to.setter
    def conforms_to(self: Distribution, conforms_to: List[str]) -> None:
        self._conforms_to = conforms_to

    @property
    def media_types(self: Distribution) -> List[str]:
        """Get/set for media_types."""
        return self._media_types

    @media_types.setter
    def media_types(self: Distribution, media_types: List[str]) -> None:
        self._media_types = media_types

    @property
    def formats(self: Distribution) -> List[str]:
        """Get/set for formats."""
        return self._formats

    @formats.setter
    def formats(self: Distribution, formats: List[str]) -> None:
        self._formats = formats

    @property
    def compression_format(self: Distribution) -> str:
        """Get/set for compression_format."""
        return self._compression_format

    @compression_format.setter
    def compression_format(self: Distribution, compression_format: str) -> None:
        self._compression_format = URI(compression_format)

    @property
    def package_format(self: Distribution) -> str:
        """Get/set for package_format."""
        return self._package_format

    @package_format.setter
    def package_format(self: Distribution, package_format: str) -> None:
        self._package_format = URI(package_format)

    # -
    def to_rdf(self: Distribution, format: str = "turtle") -> str:
        """Maps the distribution to rdf.

        Args:
            format: a valid format. Default: turtle

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding="utf-8")

    # -
    def _to_graph(self: Distribution) -> Graph:

        self._g.add((URIRef(self.identifier), RDF.type, DCAT.Distribution))

        self._title_to_graph()
        self._description_to_graph()
        self._release_date_to_graph()
        self._modification_date_to_graph()
        self._license_to_graph()
        self._access_rights_to_graph()
        self._rights_to_graph()
        self._has_policy_to_graph()
        self._access_URL_to_graph()
        self._access_service_to_graph()
        self._download_URL_to_graph()
        self._byte_size_to_graph()
        self._spatial_resolution_to_graph()
        self._temporal_resolution_to_graph()
        self._conforms_to_to_graph()
        self._media_types_to_graph()
        self._formats_to_graph()
        self._compression_format_to_graph()
        self._package_format_to_graph()

        return self._g

    def _title_to_graph(self: Distribution) -> None:
        if getattr(self, "title", None):
            for key in self._title:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

    def _description_to_graph(self: Distribution) -> None:
        if getattr(self, "description", None):
            for key in self._description:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _release_date_to_graph(self: Distribution) -> None:
        if getattr(self, "release_date", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.issued,
                    Literal(self.release_date, datatype=XSD.date),
                )
            )

    def _modification_date_to_graph(self: Distribution) -> None:
        if getattr(self, "modification_date", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.modified,
                    Literal(self.modification_date, datatype=XSD.date),
                )
            )

    def _license_to_graph(self: Distribution) -> None:
        if getattr(self, "license", None):
            self._g.add((URIRef(self.identifier), DCT.license, URIRef(self.license)))

    def _access_rights_to_graph(self: Distribution) -> None:
        if getattr(self, "access_rights", None):
            self._g.add(
                (URIRef(self.identifier), DCT.accessRights, URIRef(self.access_rights))
            )

    def _rights_to_graph(self: Distribution) -> None:
        if getattr(self, "rights", None):
            self._g.add((URIRef(self.identifier), DCT.rights, URIRef(self.rights)))

    def _has_policy_to_graph(self: Distribution) -> None:
        if getattr(self, "has_policy", None):
            self._g.add(
                (URIRef(self.identifier), ODRL.hasPolicy, URIRef(self.has_policy))
            )

    def _access_URL_to_graph(self: Distribution) -> None:
        if getattr(self, "access_URL", None):
            self._g.add(
                (URIRef(self.identifier), DCAT.accessURL, URIRef(self.access_URL))
            )

    def _access_service_to_graph(self: Distribution) -> None:
        if getattr(self, "access_service", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.accessService,
                    URIRef(self.access_service.identifier),
                )
            )

    def _download_URL_to_graph(self: Distribution) -> None:
        if getattr(self, "download_URL", None):
            self._g.add(
                (URIRef(self.identifier), DCAT.downloadURL, URIRef(self.download_URL))
            )

    def _byte_size_to_graph(self: Distribution) -> None:
        if getattr(self, "byte_size", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.byteSize,
                    Literal(self.byte_size, datatype=XSD.decimal),
                )
            )

    def _spatial_resolution_to_graph(self: Distribution) -> None:
        if getattr(self, "spatial_resolution", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.spatialResolutionInMeters,
                    Literal(self.spatial_resolution, datatype=XSD.decimal),
                )
            )

    def _temporal_resolution_to_graph(self: Distribution) -> None:
        if getattr(self, "temporal_resolution", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.temporalResolution,
                    Literal(self.temporal_resolution, datatype=XSD.duration),
                )
            )

    def _conforms_to_to_graph(self: Distribution) -> None:
        if getattr(self, "conforms_to", None):
            for _standard in self.conforms_to:
                self._g.add(
                    (URIRef(self.identifier), DCT.conformsTo, URIRef(_standard),)
                )

    def _media_types_to_graph(self: Distribution) -> None:
        if getattr(self, "media_types", None):
            for _media_type in self.media_types:
                self._g.add(
                    (URIRef(self.identifier), DCAT.mediaType, URIRef(_media_type),)
                )

    def _formats_to_graph(self: Distribution) -> None:
        if getattr(self, "formats", None):
            for _format in self.formats:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCTERMS[
                            "format"
                        ],  # https://github.com/RDFLib/rdflib/issues/932
                        URIRef(_format),
                    )
                )

    def _compression_format_to_graph(self: Distribution) -> None:
        if getattr(self, "compression_format", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.compressFormat,
                    URIRef(self._compression_format),
                )
            )

    def _package_format_to_graph(self: Distribution) -> None:
        if getattr(self, "package_format", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.packageFormat,
                    URIRef(self._package_format),
                )
            )
