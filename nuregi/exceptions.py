"""
Custom exceptions used in the project
"""


class ValidationError(Exception):
    """
    Used for any validation errors
    """

    def __init__(self, message):
        super().__init__(message)


class APIError(Exception):
    """
    Used for any API errors
    """

    def __init__(self, message):
        super().__init__(message)
