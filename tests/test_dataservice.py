from datacatalogtordf import DataService, Dataset

from rdflib import Graph
from rdflib.compare import isomorphic, graph_diff
# import pytest


def test_to_graph_should_return_endpointURL_as_graph():

    dataService = DataService()
    dataService.identifier = 'http://example.com/dataservices/1'
    dataService.endpointURL = "http://example.com/endpoints/1"

    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
        dcat:endpointURL   <http://example.com/endpoints/1>
        .
    '''
    g1 = Graph().parse(data=dataService.to_rdf(), format='turtle')
    g2 = Graph().parse(data=src, format='turtle')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_endpointDescription_as_graph():

    dataService = DataService()
    dataService.identifier = 'http://example.com/dataservices/1'
    dataService.endpointDescription = (
                "http://example.com/endpointdescription/1"
                 )

    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
        dcat:endpointDescription   <http://example.com/endpointdescription/1>
        .
    '''
    g1 = Graph().parse(data=dataService.to_rdf(), format='turtle')
    g2 = Graph().parse(data=src, format='turtle')

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_servesDataset_as_graph():

    dataService = DataService()
    dataService.identifier = 'http://example.com/dataservices/1'

    dataset1 = Dataset()
    dataset1.identifier = "http://example.com/datasets/1"
    dataService.servesdatasets.append(dataset1)

    dataset2 = Dataset()
    dataset2.identifier = "http://example.com/datasets/2"
    dataService.servesdatasets.append(dataset2)

    src = '''
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .

    <http://example.com/dataservices/1> a dcat:DataService ;
        dcat:servesDataset   <http://example.com/datasets/1>,
                             <http://example.com/datasets/2>
        .
    '''
    g1 = Graph().parse(data=dataService.to_rdf(), format='turtle')
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
