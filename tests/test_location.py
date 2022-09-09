"""Test cases for the location module."""
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization  # type: ignore

from datacatalogtordf import Location


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns a centroid graph isomorphic to spec."""
    location = Location("http://example.com/locations/1")
    location.centroid = "POINT(4.88412 52.37509)"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix locn: <http://www.w3.org/ns/locn#> .
    @prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

    <http://example.com/locations/1> a dct:Location ;
        dcat:centroid "POINT(4.88412 52.37509)"^^geosparql:asWKT ;
    .
    """
    g1 = Graph().parse(data=location.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_location_skolemized(mocker: MockFixture) -> None:
    """It returns a title graph isomorphic to spec."""
    location = Location()
    location.geometry = """POLYGON ((
          4.8842353 52.375108 , 4.884276 52.375153 ,
          4.8842567 52.375159 , 4.883981 52.375254 ,
          4.8838502 52.375109 , 4.883819 52.375075 ,
          4.8841037 52.374979 , 4.884143 52.374965 ,
          4.8842069 52.375035 , 4.884263 52.375016 ,
          4.8843200 52.374996 , 4.884255 52.374926 ,
          4.8843289 52.374901 , 4.884451 52.375034 ,
          4.8842353 52.375108
          ))"""

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix locn: <http://www.w3.org/ns/locn#> .
    @prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a dct:Location ;
        locn:geometry \"\"\"POLYGON ((
          4.8842353 52.375108 , 4.884276 52.375153 ,
          4.8842567 52.375159 , 4.883981 52.375254 ,
          4.8838502 52.375109 , 4.883819 52.375075 ,
          4.8841037 52.374979 , 4.884143 52.374965 ,
          4.8842069 52.375035 , 4.884263 52.375016 ,
          4.8843200 52.374996 , 4.884255 52.374926 ,
          4.8843289 52.374901 , 4.884451 52.375034 ,
          4.8842353 52.375108
          ))\"\"\"^^geosparql:asWKT ;
    .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=location.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_geometry_as_graph() -> None:
    """It returns a title graph isomorphic to spec."""
    location = Location()
    location.identifier = "http://example.com/locations/1"
    location.geometry = """POLYGON ((
          4.8842353 52.375108 , 4.884276 52.375153 ,
          4.8842567 52.375159 , 4.883981 52.375254 ,
          4.8838502 52.375109 , 4.883819 52.375075 ,
          4.8841037 52.374979 , 4.884143 52.374965 ,
          4.8842069 52.375035 , 4.884263 52.375016 ,
          4.8843200 52.374996 , 4.884255 52.374926 ,
          4.8843289 52.374901 , 4.884451 52.375034 ,
          4.8842353 52.375108
          ))"""

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix locn: <http://www.w3.org/ns/locn#> .
    @prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

    <http://example.com/locations/1>    a dct:Location ;
        locn:geometry \"\"\"POLYGON ((
          4.8842353 52.375108 , 4.884276 52.375153 ,
          4.8842567 52.375159 , 4.883981 52.375254 ,
          4.8838502 52.375109 , 4.883819 52.375075 ,
          4.8841037 52.374979 , 4.884143 52.374965 ,
          4.8842069 52.375035 , 4.884263 52.375016 ,
          4.8843200 52.374996 , 4.884255 52.374926 ,
          4.8843289 52.374901 , 4.884451 52.375034 ,
          4.8842353 52.375108
          ))\"\"\"^^geosparql:asWKT ;
    .
    """
    g1 = Graph().parse(data=location.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_bounding_box_as_graph() -> None:
    """It returns a bounding box graph isomorphic to spec."""
    location = Location()
    location.identifier = "http://example.com/locations/1"
    location.bounding_box = """POLYGON ((
                3.053 47.975 , 7.24  47.975 ,
                7.24  53.504 , 3.053 53.504 ,
                3.053 47.975
                ))"""

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix locn: <http://www.w3.org/ns/locn#> .
    @prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

    <http://example.com/locations/1> a dct:Location ;
        dcat:bbox \"\"\"POLYGON ((
                3.053 47.975 , 7.24  47.975 ,
                7.24  53.504 , 3.053 53.504 ,
                3.053 47.975
                ))\"\"\"^^geosparql:asWKT ;
    .
    """
    g1 = Graph().parse(data=location.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_centroid_as_graph() -> None:
    """It returns a centroid graph isomorphic to spec."""
    location = Location()
    location.identifier = "http://example.com/locations/1"
    location.centroid = "POINT(4.88412 52.37509)"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix locn: <http://www.w3.org/ns/locn#> .
    @prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

    <http://example.com/locations/1> a dct:Location ;
        dcat:centroid \"POINT(4.88412 52.37509)\"^^geosparql:asWKT ;
    .
    """
    g1 = Graph().parse(data=location.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_json_should_return_location_as_json_dict() -> None:
    """It returns a catalog json dict."""
    loc = Location()
    loc.identifier = "http://loc-identifier"
    loc.geometry = "geometry"
    loc.bounding_box = "bouding box"
    loc.centroid = "centroid"
    json = loc.to_json()

    assert json == {
        "_type": "Location",
        "bounding_box": "bouding box",
        "centroid": "centroid",
        "geometry": "geometry",
        "identifier": "http://loc-identifier",
    }


def test_from_json_should_return_location() -> None:
    """It returns a catalog json dict."""
    loc = Location()
    loc.identifier = "http://loc-identifier"
    loc.geometry = "geometry"
    loc.bounding_box = "bouding box"
    loc.centroid = "centroid"
    json = loc.to_json()

    loc_from_json = Location.from_json(json)

    g1 = Graph().parse(data=loc.to_rdf(), format="turtle")
    g2 = Graph().parse(data=loc_from_json.to_rdf(), format="turtle")

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
