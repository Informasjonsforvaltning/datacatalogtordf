"""Dataset module for mapping a dataset to rdf.

This module contains methods for mapping a dataset object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-dataset>`__

Example:
    >>> from datacatalogtordf import Dataset, Distribution
    >>>
    >>> dataset = Dataset()
    >>> dataset.identifier = "http://example.com/datasets/1"
    >>> dataset.title = {"en": "Title of dataset"}
    >>>
    >>> a_distribution = Distribution()
    >>> a_distribution.identifier = "http://example.com/dataservices/1"
    >>> a_distribution.title = {"en": "Title of distribution"}
    >>> dataset.distributions.append(a_distribution)
    >>>
    >>> bool(dataset.to_rdf())
    True
"""
from __future__ import annotations

from typing import List

from rdflib import Graph, Namespace, RDF, URIRef

from .distribution import Distribution
from .resource import Resource

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Dataset(Resource):
    """A class representing a dcat:Dataset.

    Ref: `dcat:Dataset <https://www.w3.org/TR/vocab-dcat-2/#Class:Dataset>`_.

    Attributes:
        distributions: a list of distributions of the dataset
    """

    _distributions: List

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()
        self._type = DCAT.Dataset
        self.distributions = []

    @property
    def distributions(self: Dataset) -> List[Distribution]:
        """Get/set for identifier."""
        return self._distributions

    @distributions.setter
    def distributions(self: Dataset, distributions: List[Distribution]) -> None:
        self._distributions = distributions

    # -
    def _to_graph(self: Dataset) -> Graph:

        super(Dataset, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        if hasattr(self, "distributions"):
            self._distributions_to_graph()

        return self._g

    def _distributions_to_graph(self: Dataset) -> None:

        for distribution in self._distributions:
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCAT.distribution,
                    URIRef(distribution.identifier),
                )
            )
