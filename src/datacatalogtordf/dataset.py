"""Dataset module for mapping a dataset to rdf.

This module contains methods for mapping a dataset object to rdf
according to the [dcat-ap-no v.2 standard](https://doc.difi.no/review/dcat-ap-no/)

    Typical usage example:

    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    dataset.title = {"en": "Title of dataset"}

    for distribution in listOfDistributions:
        dataset.distributions.append(distribution)

    rdf_turtle = dataservice.to_rdf()
"""
from __future__ import annotations

from typing import List

from rdflib import Graph, Namespace, RDF, URIRef

from .distribution import Distribution
from .resource import Resource

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Dataset(Resource):
    """A class representing dcat:Dataset.

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