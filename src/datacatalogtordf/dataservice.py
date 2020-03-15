from .resource import Resource
from .dataset import Dataset
from rdflib import Namespace, Graph, URIRef, RDF
from typing import List
DCT = Namespace('http://purl.org/dc/terms/')
DCAT = Namespace('http://www.w3.org/ns/dcat#')


class DataService(Resource):
    """
    A class representing dcat:DataService
    """

    def __init__(self):
        super().__init__()
        self._type = DCAT.DataService
        self.servesdatasets = []

    @property
    def endpointURL(self) -> str:
        return self._endpointURL

    @endpointURL.setter
    def endpointURL(self, endpointURL: str):
        self._endpointURL = endpointURL

    @property
    def endpointDescription(self) -> str:
        return self._endpointDescription

    @endpointDescription.setter
    def endpointDescription(self, endpointDescription: str):
        self._endpointDescription = endpointDescription

    @property
    def servesdatasets(self) -> List[Dataset]:
        return self._servesdatasets

    @servesdatasets.setter
    def servesdatasets(self, servesdatasets: List[Dataset]):
        self._servesdatasets = servesdatasets

# -
    def _to_graph(self) -> Graph:

        super(DataService, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if hasattr(self, 'endpointURL'):
            self._endpointURL_to_graph()
        if hasattr(self, 'endpointDescription'):
            self._endpointDescription_to_graph()
        if hasattr(self, 'servesdatasets'):
            self._servesdatasets_to_graph()

        return self._g
# -
    def _endpointURL_to_graph(self):

        self._g.add((URIRef(self.identifier), DCAT.endpointURL,
                     URIRef(self.endpointURL)))

    def _endpointDescription_to_graph(self):

        self._g.add((URIRef(self.identifier), DCAT.endpointDescription,
                     URIRef(self.endpointDescription)))

    def _servesdatasets_to_graph(self):

        for dataset in self._servesdatasets:
            self._g.add((URIRef(self.identifier), DCAT.servesDataset,
                         URIRef(dataset.identifier)))
