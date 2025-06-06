# src/utils/errors.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class ErrorException(Exception):
    """This is the base class for all errors"""

    pass


class InvalidToken(ErrorException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(ErrorException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(ErrorException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(ErrorException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(ErrorException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(ErrorException):
    """User has provided wrong email or password during log in."""

    pass

class UserIsInactive(ErrorException):
    """User has provided wrong email or password during log in."""

    pass

class InvalidConfirmPassword(ErrorException):
    """User has provided wrong email or password during log in."""
    
    pass

class InsufficientPermission(ErrorException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class UserNotFound(ErrorException):
    """User Not found"""

    pass


class DuplicateRecord(ErrorException):
    """Record already exists"""
    
    pass

def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: ErrorException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
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
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Credentials provided are invalid",
                "error_code": "invalid_credentials",
            },
        ),
    )

    app.add_exception_handler(
        UserIsInactive,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "User is inactive, please contact the IT department",
                "error_code": "user_inactive",
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
        InvalidConfirmPassword,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Confirm Password does not match",
                "error_code": "invalid_confirm_password",
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
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
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
        DuplicateRecord,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "Record already exists",
                "error_code": "duplicate_record",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": f"server_error: {str(exc)}",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": f"server_error: {str(exc)}",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
