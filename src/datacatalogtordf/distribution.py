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
from typing import List, Optional, TYPE_CHECKING

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
        identifier (URI): A URI uniquely identifying the resource
        title (dict): A dict with title in multiple languages
        description (dict): A free-text account of the distribution.
        release_date (Date): Date of formal issuance (e.g., publication) \
            of the distribution.
        modification_date (Date): Most recent date on which the distribution \
            was changed, updated or modified.
        license (URI): A link to legal document under which the distribution is \
            made available.
        access_rights (URI): A link to rights statement that concerns how the \
            distribution is accessed.
        rights (URI): A link to information about rights held in and over \
            the distribution.
        has_policy (URI): A link to an ODRL conformant policy expressing \
            the rights associated with the distribution.
        access_URL (URI): A URL of the resource that gives access to a \
            distribution of the dataset. E.g. landing page, feed, SPARQL endpoint.
        access_service (DataService): A data service that gives access to \
            the distribution of the dataset
        download_URL (URI): The URL of the downloadable file in a given format.\
            E.g. CSV file or RDF file. The format is indicated by \
            the distribution's dct:format and/or dcat:mediaType
        byte_size (Decimal): 	The size of a distribution in bytes.
        spatial_resolution (Decimal): 	The minimum spatial separation resolvable \
            in a dataset distribution, measured in meters.
        temporal_resolution (str): Minimum time period resolvable in the \
            dataset distribution.
        conforms_to (List[URI]): A list of links to established standards \
            to which the distribution conforms.
        media_types (List[URI]): A list of media types of the distribution \
            as defined by IANA.
        formats (List[URI]): A list of file formats of the distribution.
        compression_format (URI): The compression format of the distribution \
            in which the data is contained in a compressed form, e.g. \
            to reduce the size of the downloadable file.
        package_format (URI): The package format of the distribution in which \
            one or more data files are grouped together, e.g. to enable a set \
            of related files to be downloaded together.
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

    _g: Graph
    _identifier: URI
    _title: dict
    _description: dict
    _release_date: Date
    _modification_date: Date
    _license: URI
    _access_rights: URI
    _rights: URI
    _has_policy: URI
    _access_URL: URI
    _access_service: DataService
    _download_URL: URI
    _byte_size: Decimal
    _spatial_resolution: Decimal
    _temporal_resolution: str
    _conforms_to: List[str]
    _media_types: List[str]
    _formats: List[str]
    _compression_format: URI
    _package_format: URI

    def __init__(self) -> None:
        """Inits an object with default values."""
        self.conforms_to = []
        self.media_types = []
        self.formats = []

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
    def to_rdf(
        self: Distribution, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the distribution to rdf."""
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -
    def _to_graph(self: Distribution) -> Graph:

        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("xsd", XSD)

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
                    (
                        URIRef(self.identifier),
                        DCT.conformsTo,
                        URIRef(_standard),
                    )
                )

    def _media_types_to_graph(self: Distribution) -> None:
        if getattr(self, "media_types", None):
            for _media_type in self.media_types:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.mediaType,
                        URIRef(_media_type),
                    )
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
