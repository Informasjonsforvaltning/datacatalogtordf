"""Test cases for the distribution module."""
from decimal import Decimal

import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization

from datacatalogtordf import DataService, Distribution, InvalidURIError


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    distribution = Distribution("http://example.com/distributions/1")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a endpointURL graph isomorphic to spec."""
    distribution = Distribution()

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a dcat:Distribution ;
        .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_title_as_graph() -> None:
    """It returns a title graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.title = {"nb": "API-distribusjon", "en": "API-distribution"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:title   "API-distribution"@en, "API-distribusjon"@nb
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_description() -> None:
    """It returns a description graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.description = {"nb": "Beskrivelse", "en": "Description"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:description   "Description"@en, "Beskrivelse"@nb ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_release_date() -> None:
    """It returns a release date graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.release_date = "2019-12-31"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:issued "2019-12-31"^^xsd:date ;
    .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_modification_date() -> None:
    """It returns a modification date graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.modification_date = "2019-12-31"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:modified "2019-12-31"^^xsd:date ;
    .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_license() -> None:
    """It returns a license graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.license = "http://example.com/licenses/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:license    <http://example.com/licenses/1>
    .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_access_rights() -> None:
    """It returns a access rights graph isomorphic to spec."""
    access_rights = ["PUBLIC", "RESTRICTED", "NON-PUBLIC"]
    for _r in access_rights:
        distribution = Distribution()
        distribution.identifier = "http://example.com/distributions/1"
        distribution.access_rights = (
            f"http://publications.europa.eu/distribution/authority/access-right/{_r}"
        )

        src = (
            "@prefix dct: <http://purl.org/dc/terms/> ."
            "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> ."
            "@prefix dcat: <http://www.w3.org/ns/dcat#> .\n"
            "<http://example.com/distributions/1> a dcat:Distribution ;"
            "\tdct:accessRights\t"
            "<http://publications.europa.eu/distribution/authority/access-right/"
            f"{_r}> ."
        )
        g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
        g2 = Graph().parse(data=src, format="turtle")

        _isomorphic = isomorphic(g1, g2)
        if not _isomorphic:
            _dump_diff(g1, g2)
            pass
        assert _isomorphic


def test_to_graph_should_return_rights() -> None:
    """It returns a rights graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.rights = "http://example.com/rights/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:rights   <http://example.com/rights/1> ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_policy() -> None:
    """It returns a has_policy graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.has_policy = "http://example.com/policies/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix odrl: <http://www.w3.org/ns/odrl/2/> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        odrl:hasPolicy   <http://example.com/policies/1> ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_access_URL() -> None:
    """It returns a access URL graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.access_URL = "http://example.com/someendpoint"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:accessURL  <http://example.com/someendpoint> ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_access_service() -> None:
    """It returns a access service graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    service = DataService()
    service.identifier = "http://example.com/dataservices/1"
    distribution.access_service = service

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:accessService  <http://example.com/dataservices/1> ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_access_service_skolemized(mocker: MockFixture) -> None:
    """It returns a access service graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    service = DataService()
    distribution.access_service = service

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:accessService
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_download_URL() -> None:
    """It returns a download URL graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.download_URL = "http://example.com/download"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:downloadURL  <http://example.com/download> ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_byte_size() -> None:
    """It returns a byte size graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    # byte_size is an xsd:decimal:
    distribution.byte_size = Decimal(5120.0)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:byteSize  "5120.0"^^xsd:decimal ;
    .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_spatial_resolution_in_meters() -> None:
    """It returns a spatial resolution graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    # spatial resolution is an xsd:decimal:
    distribution.spatial_resolution_in_meters = [Decimal(30.0)]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:spatialResolutionInMeters  "30.0"^^xsd:decimal
    .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_temporal_resolution() -> None:
    """It returns a temporal resolution graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.temporal_resolution = ["PT15M"]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
            dcat:temporalResolution "PT15M"^^xsd:duration ;
    .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_conforms_to() -> None:
    """It returns a conforms to graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.conforms_to.append("http://example.com/standards/1")
    distribution.conforms_to.append("http://example.com/standards/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:conformsTo   <http://example.com/standards/1> ,
                         <http://example.com/standards/2> ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_set_conforms_to_list_of_invalid_uris() -> None:
    """Should raise InvalidURIError."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    with pytest.raises(InvalidURIError):
        distribution.conforms_to = ["http://invalid^.uri.com/format"]


def test_to_graph_should_return_media_type() -> None:
    """It returns a media type graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.media_types.append(
        "https://www.iana.org/assignments/media-types/application/ld+json"
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:mediaType \
        <https://www.iana.org/assignments/media-types/application/ld+json> ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_set_media_types_list_of_invalid_uris() -> None:
    """Should raise InvalidURIError."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    with pytest.raises(InvalidURIError):
        distribution.media_types = ["http://invalid^.uri.com/format"]


def test_to_graph_should_return_format() -> None:
    """It returns a format graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.formats.append(
        "https://www.iana.org/assignments/media-types/application/pdf"
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dct:format <https://www.iana.org/assignments/media-types/application/pdf> ;
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_compression_format() -> None:
    """It returns a compression format graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.compression_format = (
        "http://www.iana.org/assignments/media-types/application/gzip"
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:compressFormat \
            <http://www.iana.org/assignments/media-types/application/gzip>
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_packaging_format() -> None:
    """It returns a packaging format graph isomorphic to spec."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    distribution.package_format = (
        "http://publications.europa.eu/resource/authority/file-type/TAR"
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/distributions/1> a dcat:Distribution ;
        dcat:packageFormat \
            <http://publications.europa.eu/resource/authority/file-type/TAR>
        .
    """
    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_set_format_with_list_of_invalid_formats() -> None:
    """Should raise InvalidURIError."""
    distribution = Distribution()
    distribution.identifier = "http://example.com/distributions/1"
    with pytest.raises(InvalidURIError):
        distribution.formats = ["http://invalid^.uri.com/format"]


def test_to_json_should_return_distribution_as_json_dict() -> None:
    """It returns a catalog json dict."""

    dist = Distribution()
    dist.identifier = "http://distribution-identifier"
    dist.title = {"en": "dist title"}
    dist.description = {"en": "dist description"}
    dist.formats = ["http://csv", "http://xml"]
    dist.license = "http://license"

    json = dist.to_json()

    assert json == {
        "_type": "Distribution",
        "conforms_to": [],
        "description": {"en": "dist description"},
        "formats": ["http://csv", "http://xml"],
        "identifier": "http://distribution-identifier",
        "license": "http://license",
        "media_types": [],
        "title": {"en": "dist title"},
    }


def test_from_json_should_return_distribution() -> None:
    """It returns a distribution."""

    data_service = DataService()
    data_service.identifier = "http://data-service-identifier"

    distribution = Distribution()
    distribution.identifier = "http://distribution-identifier"
    distribution.title = {"en": "distribution title"}
    distribution.description = {"en": "distribution description"}
    distribution.access_service = data_service

    json = distribution.to_json()

    distribution_from_json = Distribution.from_json(json)

    g1 = Graph().parse(data=distribution.to_rdf(), format="turtle")
    g2 = Graph().parse(data=distribution_from_json.to_rdf(), format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Utils for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="turtle").splitlines():
        if _l:
            print(_l)
