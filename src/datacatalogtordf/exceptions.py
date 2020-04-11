"""Exeptions module for datacatalogtordf."""

__all__ = ["Error", "InvalidDateError", "InvalidDateIntervalError"]


class Error(Exception):
    """Base class for exceptions."""

    def __init__(self, msg: str = None) -> None:
        """Inits the exception."""
        Exception.__init__(self, msg)
        self.msg = msg


class InvalidDateError(Error):
    """Exception raised for errors in the input.

    Attributes:
        str -- input str in which the error occurred
        message -- explanation of the error
    """

    __slots__ = ()

    def __init__(self, date: str, msg: str) -> None:
        """Inits the exception."""
        Error.__init__(self, msg)
        self.date = date
        self.message = msg


class InvalidDateIntervalError(Error):
    """Exception raised for errors in the input.

    Attributes:
        str -- input str in which the error occurred
        message -- explanation of the error
    """

    __slots__ = ()

    def __init__(self, start_date: str, end_date: str, msg: str) -> None:
        """Inits the exception."""
        Error.__init__(self, msg)
        self.start_date = start_date
        self.end_date = end_date
        self.message = msg


class InvalidURIError(Error):
    """Exception raised for errors in the input.

    Attributes:
        str -- input str in which the error occurred
        message -- explanation of the error
    """

    __slots__ = ()

    def __init__(self, string: str, message: str) -> None:
        """Inits the exception."""
        self.str = str
        self.message = message
