"""Datacatalog package.

Modules:
    resource
    dataset
    dataset_series
    catalog
    dataservice
    distribution
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .agent import Agent
from .catalog import Catalog
from .catalogrecord import CatalogRecord
from .contact import Contact
from .dataservice import DataService
from .dataset import Dataset
from .dataset_series import DatasetSeries
from .distribution import Distribution
from .document import Document
from .exceptions import InvalidDateError, InvalidDateIntervalError
from .location import Location
from .periodoftime import PeriodOfTime
from .relationship import Relationship
from .resource import Resource
from .uri import InvalidURIError, URI

__all__ = [
    "Agent",
    "Catalog",
    "CatalogRecord",
    "Contact",
    "DataService",
    "Dataset",
    "DatasetSeries",
    "Distribution",
    "Document",
    "InvalidDateError",
    "InvalidDateIntervalError",
    "Location",
    "PeriodOfTime",
    "Relationship",
    "Resource",
    "InvalidURIError",
    "URI",
]
