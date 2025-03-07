# src/utils/dependency.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .security import verify_token
from .errors import (
    InvalidToken,
    RevokedToken,
    RefreshTokenRequired,
    AccessTokenRequired,
)
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.databases.redis import RedisDB
from typing import List, Optional
from src.utils.logging import Logging
import logging
from src.databases import db

redisDB = RedisDB()
logger = Logging(level="DEBUG")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        try:
            data = await super(JWTBearer, self).__call__(request)
            token = data.credentials

            user = verify_token(token)

            if not self.is_valid_token(token):
                raise InvalidToken

            if await redisDB.token_in_blocklist(user["jti"]):
                logger.log("warning", f"Token {user['jti']} is revoked")
                raise RevokedToken

            self.verify(user)

            return user

        except HTTPException as e:
            raise e
        except RevokedToken as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Token has been revoked",
                    "resolution": "Please get new token",
                    "error_code": "token_revoked",
                },
            )
        except InvalidToken as e:
            raise e
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    def is_valid_token(self, token: str) -> bool:
        token = verify_token(token)

        return True if token is not None else False

    def verify(self, token: dict) -> None:
        raise NotImplementedError("You must implement this method in your subclass")


class AccessTokenBearer(JWTBearer):
    def verify(self, token: dict) -> None:
        if token["refresh"]:
            raise AccessTokenRequired

        return True


class RefreshTokenBearer(JWTBearer):
    def verify(self, token: dict) -> None:
        if not token["refresh"]:
            raise RefreshTokenRequired

        return True


class AccessControlBearer(AccessTokenBearer):
    def __init__(
        self,
        auto_error: bool = True,
        menu_names: List[str] = [],
        permissions: List[str] = [],
    ):
        super(AccessControlBearer, self).__init__(auto_error=auto_error)
        self.menu_names = menu_names
        self.permissions = permissions

    async def __call__(
        self, request: Request, session: AsyncSession = Depends(db.session)
    ) -> HTTPAuthorizationCredentials:
        try:

            if token := await super(AccessControlBearer, self).__call__(request):
                # call class UserPermissionBearer if role permission not found
                access_control = await RolePermissionBearer(
                    auto_error=True, permissions=self.permissions
                )(request, session)

                if not access_control:
                    access_control = await UserPermissionBearer(
                        auto_error=True, permissions=self.permissions
                    )(request, session)
                    # return True  # just for development

                return token

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}",
            )

    def verify(self, token: dict) -> None:
        if token["refresh"]:
            raise AccessTokenRequired

        return True


class RolePermissionBearer(AccessTokenBearer):
    def __init__(self, auto_error: bool = True, permissions: List[str] = []):
        super(RolePermissionBearer, self).__init__(auto_error=auto_error)
        self.permissions = permissions

    async def __call__(
        self, request: Request, session: AsyncSession = Depends(db.session)
    ) -> HTTPAuthorizationCredentials:
        try:
            from src.modules.authentications.roles.models import (
                RolePermission,
            )
            from src.modules.authentications.roles.models import Role
            from src.modules.authentications.permissions.models import Permission
            from sqlalchemy.orm import joinedload
            from sqlmodel import select

            # logger.log("warning", f"Permission required: {self.permissions}")
            # logger.log(
            #     "warning",
            #     f"RoleID required: {request.state.authorize['user']['role_id']}",
            # )

            if token := await super(RolePermissionBearer, self).__call__(request):
                # with where in permission
                q = (
                    select(RolePermission)
                    .join(Role)
                    .join(Permission)
                    .options(
                        joinedload(RolePermission.role),
                        joinedload(RolePermission.permission),
                    )
                    .where(Permission.name.in_(self.permissions))
                    .where(Role.id == token["user"]["role_id"])
                )
                result = await session.execute(q)
                access = result.scalars().first()

                if not access:
                    return False

                return token

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}",
            )

    def verify(self, token: dict) -> None:
        if token["refresh"]:
            raise AccessTokenRequired

        return True


class UserPermissionBearer(JWTBearer):
    def __init__(self, auto_error: bool = True, permissions: List[str] = []):
        super(UserPermissionBearer, self).__init__(auto_error=auto_error)
        self.permissions = permissions

    async def __call__(
        self, request: Request, session: AsyncSession = Depends(db.session)
    ) -> HTTPAuthorizationCredentials:
        try:
            from src.modules.authentications.users.models import (
                UserPermission,
            )
            from src.modules.authentications.users.models import User
            from src.modules.authentications.permissions.models import Permission
            from sqlalchemy.orm import joinedload
            from sqlmodel import select

            if token := await super(UserPermissionBearer, self).__call__(request):
                # with where in permission
                q = (
                    select(UserPermission)
                    .join(User)
                    .join(Permission)
                    .options(
                        joinedload(UserPermission.user),
                        joinedload(UserPermission.permission),
                    )
                    .where(Permission.name.in_(self.permissions))
                    .where(User.id == token["user"]["id"])
                )
                result = await session.execute(q)
                access = result.scalars().first()

                if not access:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={
                            "message": "Forbidden",
                            "detail": "This role does not have permission to access this resource or You don't have permission to access this resource",
                            "resolution": "Please contact your administrator or IT support",
                        },
                    )

                return token

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}",
            )

    def verify(self, token: dict) -> None:
        if token["refresh"]:
            raise AccessTokenRequired

        return True
