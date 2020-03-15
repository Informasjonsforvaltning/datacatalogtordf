from __future__ import annotations

from typing import List

from rdflib import Graph, Namespace, RDF, URIRef

from .dataset import Dataset
from .resource import Resource

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class DataService(Resource):
    """
    A class representing dcat:DataService
    """

    _endpointURL: str
    _endpointDescription: str
    _servesdatasets: List

    def __init__(self) -> None:
        super().__init__()
        self._type = DCAT.DataService
        self.servesdatasets = []

    @property
    def endpointURL(self: DataService) -> str:
        return self._endpointURL

    @endpointURL.setter
    def endpointURL(self: DataService, endpointURL: str) -> None:
        self._endpointURL = endpointURL

    @property
    def endpointDescription(self: DataService) -> str:
        return self._endpointDescription

    @endpointDescription.setter
    def endpointDescription(self: DataService, endpointDescription: str) -> None:
        self._endpointDescription = endpointDescription

    @property
    def servesdatasets(self: DataService) -> List[Dataset]:
        return self._servesdatasets

    @servesdatasets.setter
    def servesdatasets(self: DataService, servesdatasets: List[Dataset]) -> None:
        self._servesdatasets = servesdatasets

    # -
    def _to_graph(self: DataService) -> Graph:

        super(DataService, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if getattr(self, "endpointURL", None):
            self._endpointURL_to_graph()
        if getattr(self, "endpointDescription", None):
            self._endpointDescription_to_graph()
        if getattr(self, "servesdatasets", None):
            self._servesdatasets_to_graph()

        return self._g

    # -
    def _endpointURL_to_graph(self: DataService) -> None:

        self._g.add(
            (URIRef(self.identifier), DCAT.endpointURL, URIRef(self.endpointURL))
        )

    def _endpointDescription_to_graph(self: DataService) -> None:

        self._g.add(
            (
                URIRef(self.identifier),
                DCAT.endpointDescription,
                URIRef(self.endpointDescription),
            )
        )

    def _servesdatasets_to_graph(self: DataService) -> None:

        for dataset in self._servesdatasets:
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.servesDataset,
                    URIRef(dataset.identifier),
                )
            )
