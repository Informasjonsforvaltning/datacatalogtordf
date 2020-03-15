from typing import List

from rdflib import Graph, Namespace, RDF, URIRef

from .distribution import Distribution
from .resource import Resource

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Dataset(Resource):
    """
    A class representing dcat:Dataset
    """

    def __init__(self):
        super().__init__()
        self._type = DCAT.Dataset
        self.distributions = []

    @property
    def distributions(self) -> List[Distribution]:
        return self._distributions

    @distributions.setter
    def distributions(self, distributions: List[Distribution]):
        self._distributions = distributions

    # -
    def _to_graph(self) -> Graph:

        super(Dataset, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if hasattr(self, "distributions"):
            self._distributions_to_graph()

        return self._g

    def _distributions_to_graph(self):

        for distribution in self._distributions:
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.distribution,
                    URIRef(distribution.identifier),
                )
            )
