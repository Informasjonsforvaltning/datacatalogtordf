from rdflib import Graph, Literal, Namespace, RDF, URIRef

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Distribution:
    """
    A class representing dcat:Distribution
    """

    def __init__(self):
        self._type = DCAT.Distribution
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        self._identifier = identifier

    @property
    def title(self) -> dict:
        return self._title

    @title.setter
    def title(self, title: dict):
        self._title = title

    # -
    def to_rdf(self, format="turtle") -> str:
        """
        Maps the distribution to rdf and returns a serialization
           as a string according to format
        """

        return self._to_graph().serialize(format=format, encoding="utf-8")

    # -
    def _to_graph(self) -> Graph:

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if hasattr(self, "title"):
            self._title_to_graph()

        return self._g

    def _title_to_graph(self):

        for key in self._title:
            self._g.add(
                (URIRef(self.identifier), DCT.title, Literal(self.title[key], lang=key))
            )
