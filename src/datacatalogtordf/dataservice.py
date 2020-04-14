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

    _endpointURL: List[URI]
    _endpointDescription: List[URI]
    _servesdatasets: List[Dataset]

    def __init__(self) -> None:
        """Inits DataService with default values."""
        super().__init__()
        self._type = DCAT.DataService
        self.endpointURL = []
        self.endpointDescription = []
        self.servesdatasets = []

    @property
    def endpointURL(self: DataService) -> List[URI]:
        """Get/set for endpointURL."""
        return self._endpointURL

    @endpointURL.setter
    def endpointURL(self: DataService, endpointURL: List[URI]) -> None:
        self._endpointURL = endpointURL

    @property
    def endpointDescription(self: DataService) -> List[URI]:
        """Get/set for endpointDescription."""
        return self._endpointDescription

    @endpointDescription.setter
    def endpointDescription(self: DataService, endpointDescription: List[URI]) -> None:
        self._endpointDescription = endpointDescription

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

        self._endpointURL_to_graph()
        self._endpointDescription_to_graph()
        self._servesdatasets_to_graph()

        return self._g

    # -
    def _endpointURL_to_graph(self: DataService) -> None:
        if getattr(self, "endpointURL", None):
            for _endpointURL in self.endpointURL:
                self._g.add(
                    (URIRef(self.identifier), DCAT.endpointURL, URIRef(_endpointURL))
                )

    def _endpointDescription_to_graph(self: DataService) -> None:
        if getattr(self, "endpointDescription", None):
            for _endpointDescription in self.endpointDescription:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.endpointDescription,
                        URIRef(_endpointDescription),
                    )
                )

    def _servesdatasets_to_graph(self: DataService) -> None:
        if getattr(self, "servesdatasets", None):
            for dataset in self._servesdatasets:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCAT.servesDataset,
                        URIRef(dataset.identifier),
                    )
                )
