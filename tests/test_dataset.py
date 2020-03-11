from datacatalogtordf.catalog import Dataset
from datacatalogtordf.distribution import Distribution

from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff
# import pytest


def test_to_graph_should_return_publisher_as_graph():

    catalog = Dataset()
    catalog.identifier = 'http://example.com/catalogs/1'
    catalog.publisher = 'http://example.com/publisher/1'

    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Dataset ;
        dct:publisher   <http://example.com/publisher/1> ;
        .
    '''
    g1 = Graph().parse(data=catalog.to_rdf(), format='turtle')
    g2 = Graph().parse(data=src, format='turtle')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_title_as_graph():

    catalog = Dataset()
    catalog.identifier = 'http://example.com/catalogs/1'
    catalog.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/catalogs/1> a dcat:Dataset ;
        dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
    '''
    g1 = Graph().parse(data=catalog.to_rdf(), format='turtle')
    g2 = Graph().parse(data=src, format='turtle')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_distribution_as_graph():

    catalog = Dataset()
    catalog.identifier = 'http://example.com/datasets/1'

    distribution1 = Distribution()
    distribution1.identifier = 'http://example.com/distributions/1'
    catalog.distributions.append(distribution1)

    distribution2 = Distribution()
    distribution2.identifier = 'http://example.com/distributions/2'
    catalog.distributions.append(distribution2)

    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/datasets/1> a dcat:Dataset ;
        dcat:distribution   <http://example.com/distributions/1>,
                            <http://example.com/distributions/2>
        .
    '''
    g1 = Graph().parse(data=catalog.to_rdf(), format='turtle')
    g2 = Graph().parse(data=src, format='turtle')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic
# ---------------------------------------------------------------------- #
# Utils for displaying debug information


def _dump_diff(g1, g2):
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle_sorted(g):
    for l in sorted(g.serialize(format='turtle').splitlines()):
        if l:
            print(l.decode())


def _dump_turtle(g):
    for l in g.serialize(format='turtle').splitlines():
        if l:
            print(l.decode())
