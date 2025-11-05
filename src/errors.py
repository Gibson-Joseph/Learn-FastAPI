from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BookStoreException(Exception):  # This is a Python exceptions
    """This is the base class for all bookstore errors"""

    pass


class InvalidToken(BookStoreException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BookStoreException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(BookStoreException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefereshTokenRequired(BookStoreException):
    """User has provided a access token when an referesh token is needed"""

    pass


class UserAlreadyExists(BookStoreException):
    """User has provided an email for a user who exists during sign up"""

    pass


class InvalidCredentials(BookStoreException):
    """User has provided wrong email or password during log in"""

    pass


class InsufficientPermission(BookStoreException):
    """User does not have the necessary permissions to perform an action"""

    pass


class BookNotFound(BookStoreException):
    """Book Not found"""

    pass


class TagNotFound(BookStoreException):
    """Tag Not found"""

    pass


class TagAlreadyExists(BookStoreException):
    """Tag already exists"""

    pass


class UserNotFound(BookStoreException):
    """User Not found"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    # In Python, typing.Callable is a type hint used to specify that a variable, parameter, or return value should be a function (or any callable object) — i.e., something you can call with parentheses () like a regular function.

    # The first part (inside [ ]) defines the types of arguments the callable takes.
    # The second part (after ,) defines the return type.

    async def exception_handler(requst: Request, exc: BookStoreException):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code,
        )

    return exception_handler
