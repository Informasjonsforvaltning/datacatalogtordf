"""Datacatalog package.

Modules:
    resource
    dataset
    catalog
    dataservice
    distribution
"""
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .agent import Agent
from .catalog import Catalog
from .catalogrecord import CatalogRecord
from .dataservice import DataService
from .dataset import Dataset
from .distribution import Distribution
from .document import Document
from .exceptions import InvalidDateError, InvalidDateIntervalError
from .location import Location
from .periodoftime import PeriodOfTime
from .relationship import Relationship
from .resource import Resource
from .uri import InvalidURIError, URI
