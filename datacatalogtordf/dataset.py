from rdflib import Graph, Namespace, RDF, URIRef, Literal
DCT = Namespace('http://purl.org/dc/terms/')
DCAT = Namespace('http://www.w3.org/ns/dcat#')


class Dataset:
    """
    A class representing dcat:Dataset
    """

    def __init__(self):
        self._type = DCAT.Dataset
        # set up graph and namespaces:
        self._g = Graph()
        self._g.bind('dct', DCT)
        self._g.bind('dcat', DCAT)

    @property
    def publisher(self) -> str:
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: str):
        self._publisher = publisher

    @property
    def title(self) -> dict:
        return self._title

    @title.setter
    def title(self, title: dict):
        self._title = title
# -

    def to_rdf(self, format='turtle') -> str:
        """Maps the dataset to rdf and returns a serialization
           as a string according to format"""

        return self._to_graph().serialize(format=format, encoding='utf-8')
# -
    def _to_graph(self) -> Graph:

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if hasattr(self, 'publisher'):
            self._publisher_to_graph()
        if hasattr(self, 'title'):
            self._title_to_graph()

        return self._g

    def _publisher_to_graph(self):

        self._g.add((URIRef(self.identifier), DCT.publisher,
                     URIRef(self.publisher)))

    def _title_to_graph(self):

        for key in self._title:
            self._g.add((URIRef(self.identifier), DCT.title,
                         Literal(self.title[key], lang=key)))
