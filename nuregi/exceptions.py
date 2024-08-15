"""Custom exceptions."""


class ValidationError(Exception):
    """Used for validation errors."""

    def __init__(self, message: str) -> None:
        """Initialise the exception."""
        super().__init__(message)


class APIError(Exception):
    """Used for API errors."""

    def __init__(self, message: str) -> None:
        """Initialise the exception."""
        super().__init__(message)


class ParsingError(Exception):
    """Used for parsing errors."""

    def __init__(self, message: str) -> None:
        """Initialise the exception."""
        super().__init__(message)
