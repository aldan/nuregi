"""Common functions for parsing."""

from functools import wraps


def validate_return_as(valid_options: list[str]):
    """Validate return type options."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return_as = kwargs.get("return_as")
            if return_as not in valid_options and return_as is not None:
                msg = f"Invalid value for 'return_as': '{return_as}'. Expected one of {valid_options}."
                raise ValueError(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator
