"""
Custom exceptions for pdf package
"""


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
