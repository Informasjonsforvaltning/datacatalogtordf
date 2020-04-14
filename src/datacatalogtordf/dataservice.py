"""DataService module for mapping a dataService to rdf.

This module contains methods for mapping a dataservice object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-datatjeneste>`__

Example:
    >>> from datacatalogtordf import DataService
    >>>
    >>> dataservice = DataService()
    >>> dataservice.identifier = "http://example.com/dataservices/1"
    >>> dataservice.title = {"en": "Title of dataservice"}
    >>>
    >>> bool(dataservice.to_rdf())
    True
"""
from __future__ import annotations

from typing import List

from rdflib import Graph, Namespace, RDF, URIRef

from .dataset import Dataset
from .resource import Resource
from .uri import URI

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class DataService(Resource):
    """A class representing a dcat:DataService.

    Ref: `dcat:DataService <https://www.w3.org/TR/vocab-dcat-2/#Class:Data_Service>`_.

    Attributes:
        endpointURL: The root location or primary endpoint of the service
         (a Web-resolvable IRI).
        endpointDescription: A description of the services available via
        the end-points, including their operations, parameters etc.
    """

    _endpointURL: URI
    _endpointDescription: URI
    _servesdatasets: List

    def __init__(self) -> None:
        """Inits DataService with default values."""
        super().__init__()
        self._type = DCAT.DataService
        self.servesdatasets = []

    @property
    def endpointURL(self: DataService) -> str:
        """Get/set for endpointURL."""
        return self._endpointURL

    @endpointURL.setter
    def endpointURL(self: DataService, endpointURL: str) -> None:
        self._endpointURL = URI(endpointURL)

    @property
    def endpointDescription(self: DataService) -> str:
        """Get/set for endpointDescription."""
        return self._endpointDescription

    @endpointDescription.setter
    def endpointDescription(self: DataService, endpointDescription: str) -> None:
        self._endpointDescription = URI(endpointDescription)

    @property
    def servesdatasets(self: DataService) -> List[Dataset]:
        """Get/set for servesdatasets."""
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
