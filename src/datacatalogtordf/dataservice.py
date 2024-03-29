"""DataService module for mapping a dataService to rdf.

This module contains methods for mapping a dataservice object to rdf
according to the
`dcat-ap-no v.2 standard <https://data.norge.no/specification/dcat-ap-no/#klasse-datatjeneste>`__

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

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from rdflib import Graph, Namespace, RDF, URIRef
from skolemizer import Skolemizer

from .dataset import Dataset
from .resource import Resource
from .uri import URI

if TYPE_CHECKING:  # pragma: no cover
    pass

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class DataService(Resource):
    """A class representing a dcat:DataService.

    Args:
        identifier (URI): the identifier of the datasetservice.

    Ref: `dcat:DataService <https://www.w3.org/TR/vocab-dcat-2/#Class:Data_Service>`_.
    """

    _endpointURL: URI
    _endpointDescription: URI
    _servesdatasets: List[Dataset]
    _media_types: List[str]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits DataService with default values."""
        super().__init__()

        if identifier:
            self.identifier = identifier

        self._type = DCAT.DataService
        self.servesdatasets = []
        self.media_types = []

    @property
    def endpointURL(self: DataService) -> str:
        """URI: The root location or primary endpoint of the service (a Web-resolvable IRI)."""
        return self._endpointURL

    @endpointURL.setter
    def endpointURL(self: DataService, endpointURL: str) -> None:
        self._endpointURL = URI(endpointURL)

    @property
    def endpointDescription(self: DataService) -> str:
        """URI: A description of the services available via the end-points, including their operations, parameters etc."""
        # noqa: B950
        return self._endpointDescription

    @endpointDescription.setter
    def endpointDescription(self: DataService, endpointDescription: str) -> None:
        self._endpointDescription = URI(endpointDescription)

    @property
    def servesdatasets(self: DataService) -> List[Dataset]:
        """List[Dataset]: A list of datasets that this service serves."""
        return self._servesdatasets

    @servesdatasets.setter
    def servesdatasets(self: DataService, servesdatasets: List[Dataset]) -> None:
        self._servesdatasets = servesdatasets

    @property
    def media_types(self: DataService) -> List[str]:
        """List[src]: A list of media types that is offered in the responses."""
        return self._media_types

    @media_types.setter
    def media_types(self: DataService, media_types: List[str]) -> None:
        self._media_types = media_types

    # -
    @classmethod
    def from_json(cls, json: Dict) -> Resource:
        """Convert a JSON (dict).

        Args:
            json: A dict representing this class.

        Returns:
            Resource: The object.
        """
        resource = cls()
        for key in json:
            is_private = key.startswith("_")
            if not is_private:
                v = json[key]
                if isinstance(v, list):
                    alist = []
                    for i in v:
                        attr = cls._attr_from_json(key, i)
                        if attr is not None:
                            alist.append(attr)
                        else:
                            alist.append(i)
                    setattr(resource, key, alist)
                else:
                    setattr(resource, key, v)

        return resource

    def _to_graph(self: DataService) -> Graph:

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        super(DataService, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if getattr(self, "endpointURL", None):
            self._endpointURL_to_graph()
        if getattr(self, "endpointDescription", None):
            self._endpointDescription_to_graph()
        if getattr(self, "servesdatasets", None):
            self._servesdatasets_to_graph()
        if getattr(self, "media_types", None):
            self._media_type_to_graph()

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

            if not getattr(dataset, "identifier", None):
                dataset.identifier = Skolemizer.add_skolemization()

            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.servesDataset,
                    URIRef(dataset.identifier),
                )
            )

    def _media_type_to_graph(self: DataService) -> None:

        for _media_type in self.media_types:
            self._g.add((URIRef(self.identifier), DCAT.mediaType, URIRef(_media_type)))

    @classmethod
    def _attr_from_json(cls, attr: str, json_dict: Dict) -> Any:
        obj = Resource._attr_from_json(attr, json_dict)
        if obj is not None:
            return obj

        if attr == "servesdatasets":
            return Dataset.from_json(json_dict)

        return None
