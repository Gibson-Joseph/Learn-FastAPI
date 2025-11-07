from typing import Any, Callable
from fastapi import FastAPI, status
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


class AccountNotVerified(BookStoreException):
    """Account not yet verified"""

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


def register_error_handlers(app: FastAPI):
    # In FastAPI, app.add_exception_handler() lets you register a custom handler for specific exceptions.

    # That means:

    # Whenever that specific exception is raised anywhere in your app, FastAPI will catch it and use your custom handler function to generate the HTTP response instead of crashing or returning the default error.

    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "user not found",
                "error_code": "user_not_found",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )

    app.add_exception_handler(
        RefereshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid referesh token",
                "resolution": "Please get an referesh token",
                "error_code": "referesh_token_required",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Tag Not Found", "error_code": "tag_not_found"},
        ),
    )

    app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Tag Already exists",
                "error_code": "tag_exists",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book Not Found",
                "error_code": "book_not_found",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not Verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
