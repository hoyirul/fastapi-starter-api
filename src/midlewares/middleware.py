# src/middlewares/middleware.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.utils.logging import Logging
from fastapi.responses import JSONResponse
import time
from src.utils.dependency import AccessTokenBearer
from fastapi.exceptions import HTTPException
import socket

logger = Logging(level="DEBUG")
"""
Middleware class to handle all middleware for the FastAPI application,
You can add more middleware to this class as needed.
"""


class Middleware:
    def __init__(self, app: FastAPI, parent_url: str = "/api/v1"):
        self.app = app
        self.parent_url = parent_url
        self.version = parent_url.split("/")[-1]

    # Determine the log level based on the status code
    def level(self, status_code: int):
        level = "info"
        if status_code >= 500:
            level = "critical"
        elif status_code >= 400:
            level = "error"
        elif status_code >= 300:
            level = "warning"
        elif status_code >= 200:
            level = "info"
        return level

    # Register middleware for the FastAPI application
    def register_middleware(self):
        @self.app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            start_time = time.time()

            response = await call_next(request)

            process_time = time.time() - start_time

            level = self.level(response.status_code)

            logger.log(
                level,
                f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} - completed after {process_time}s",
            )

            return response

        # Add Authorization middleware to check for the Authorization header
        @self.app.middleware("http")
        async def authorization(request: Request, call_next):
            try:
                # Skip the Authorization check for the /auth/login and /auth/register paths
                if ExceptRoute(parent_url=self.parent_url).except_route(request):
                    response = await call_next(request)
                    return response

                if "Authorization" not in request.headers:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "message": "Unauthorized",
                            "resolution": "Please provide an Authorization header",
                        },
                    )

                # get current user
                authorize = await AccessTokenBearer()(request)
                if authorize:
                    request.state.authorize = authorize
                    hostname = socket.gethostname()
                    request.state.authorize["ip_address"] = socket.gethostbyname(
                        hostname
                    )

                response = await call_next(request)
                return response
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code, content={"detail": e.detail}
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": "Internal server error", "error": str(e)},
                )

        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Add TrustedHostMiddleware
        self.app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])


"""
For handling exceptions, you can create a class that inherits from the Exception class.
/docs, /redoc, and /openapi/{version}.json are paths that do not require authorization.
"""


class ExceptRoute:
    def __init__(self, parent_url: str = "/api/v1"):
        self.parent_url = parent_url
        self.version = parent_url.split("/")[-1]

    def except_route(self, request: Request):
        if request.url.path in [
            "/",
            "/favicon.ico",
            "/docs",
            "/redoc",
            f"/openapi/{self.version}.json",
            "/docs/convention-id.md",
            "/docs/convention-en.md",
            f"{self.parent_url}/auth/login",
            f"{self.parent_url}/auth/register",
        ]:
            return True
        return False
