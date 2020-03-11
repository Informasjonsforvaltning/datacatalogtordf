from .dataset import Dataset
from typing import List

from rdflib import Graph, Namespace, RDF, URIRef

DCT = Namespace('http://purl.org/dc/terms/')
DCAT = Namespace('http://www.w3.org/ns/dcat#')


class Catalog(Dataset):
    """
    A class representing dcat:Catalog
    """

    def __init__(self):
        super().__init__()
        self._type = DCAT.Catalog
        self.datasets = []

    @property
    def datasets(self) -> List[Dataset]:
        return self._datasets

    @datasets.setter
    def datasets(self, datasets: List[Dataset]):
        self._datasets = datasets
# -
    def _to_graph(self) -> Graph:

        super(Catalog, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if hasattr(self, 'datasets'):
            self._datasets_to_graph()

        return self._g

    def _datasets_to_graph(self):

        for dataset in self._datasets:
            self._g.add((URIRef(self.identifier), DCAT.dataset,
                         URIRef(dataset.identifier)))
