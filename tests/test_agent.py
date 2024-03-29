"""Test cases for the agent module."""
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
from skolemizer.testutils import skolemization

from datacatalogtordf import Agent, Dataset
from tests.testutils import assert_isomorphic


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns a identifier graph isomorphic to spec."""
    agent = Agent("http://example.com/agents/1")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/agents/1> a foaf:Agent .
    """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a agent graph as with skolemization node isomorphic to spec."""
    agent = Agent()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .


        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a foaf:Agent  .

        """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_name_as_graph() -> None:
    """It returns a title graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.name = {"en": "James Bond", "nb": "Djeims Bånd"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <http://example.com/agents/1>    a foaf:Agent ;
        foaf:name "James Bond"@en, "Djeims Bånd"@nb ;
    .
    """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_publisher_as_bnode() -> None:
    """It returns a name graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    agent = Agent()
    agent.name = {"en": "James Bond", "nb": "Djeims Bånd"}
    dataset.publisher = agent

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <http://example.com/datasets/1> a dcat:Dataset;
    dct:publisher   [a foaf:Agent ;
                       foaf:name "James Bond"@en, "Djeims Bånd"@nb ;
                    ] ;
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _dump_turtle(g1)
    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_organizationid_as_graph() -> None:
    """It returns a organization_id graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.organization_id = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <http://example.com/agents/1>    a foaf:Agent ;
        dct:identifier "123456789";
    .
    """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_organization_type_as_graph() -> None:
    """It returns a type graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.organization_type = "http://example.com/concepts/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <http://example.com/agents/1>    a foaf:Agent ;
        dct:type <http://example.com/concepts/1>;
    .
    """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_same_as() -> None:
    """It returns a agent graph isomorphic to spec."""
    """It returns an sameAs graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.same_as = "http://example.com/agents/2"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    <http://example.com/agents/1> a foaf:Agent ;
        owl:sameAs <http://example.com/agents/2> ;
        .
        """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_json_should_return_partial_agent_as_json_dict() -> None:
    """It returns a agent json dict."""
    agent = Agent()
    agent.identifier = "http://example.com/agent/1"

    json = agent.to_json()

    assert json == {
        "_type": "Agent",
        "identifier": "http://example.com/agent/1",
    }


def test_to_json_should_return_agent_as_json_dict() -> None:
    """It returns a agent json dict."""
    agent = Agent()
    agent.identifier = "http://example.com/agent/1"
    agent.name = {"nb": "Agent A", "en": "Agent A"}
    agent.organization_id = "org-id"
    agent.organization_type = "http://org-type"
    agent.same_as = "http://same-as"

    json = agent.to_json()

    assert json == {
        "_type": "Agent",
        "identifier": "http://example.com/agent/1",
        "name": {"nb": "Agent A", "en": "Agent A"},
        "organization_id": "org-id",
        "organization_type": "http://org-type",
        "same_as": "http://same-as",
    }


def test_from_json_should_return_agent() -> None:
    """It returns a agent instance."""
    agent = Agent()
    agent.identifier = "http://example.com/agent/1"
    agent.name = {"nb": "Agent A", "en": "Agent A"}
    agent.organization_id = "org-id"
    agent.organization_type = "http://org-type"
    agent.same_as = "http://same-as"

    json = agent.to_json()

    agent_from_json = Agent.from_json(json)

    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=agent_from_json.to_rdf(), format="turtle")

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
