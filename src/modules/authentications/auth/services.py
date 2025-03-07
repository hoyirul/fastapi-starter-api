# src/modules/authentications/auth/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
    LoginRequestSchema, 
    RegisterRequestSchema, 
    SwitchAccountRequestSchema,
    AuthSchema,
    ChangePasswordRequestSchema
)
from sqlalchemy import select
from .models import Auth
from src.modules.authentications.roles.models import Role
from src.modules.authentications.users.models import UserRole
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.utils.security import (
    password_hash,
    verify_password,
    generate_token,
)
from datetime import timedelta, datetime
from src.configs import Config
from src.databases.redis import RedisDB
from src.utils.errors import (
    InvalidCredentials,
    UserAlreadyExists,
    UserNotFound,
    InvalidToken,
    InvalidConfirmPassword,
    UserIsInactive
)
from sqlalchemy.orm import selectinload, joinedload
from src.utils.logging import Logging

redisDB = RedisDB()


class AuthService:
    def __init__(self):
        self.logger = Logging(level="DEBUG")

    async def login(self, request: LoginRequestSchema, session: AsyncSession) -> dict:
        user = await self.user_exists(request.email, session)

        # check is user active
        if not await self.is_active(request.email, session):
            raise UserIsInactive

        last_logged_in = await self.last_logged_in(request.email, session)

        user.last_logged_in = last_logged_in
        
        password = verify_password(request.password, user.password)
        if not password:
            raise InvalidCredentials

        access_token = generate_token(
            data=jsonable_encoder(user),
        )

        refresh_token = generate_token(
            data=jsonable_encoder(user),
            expiry=timedelta(seconds=Config.JWT_REFRESH_EXPIRY),
            refresh=True,
        )

        return JSONResponse(
            content={
                "success": True,
                "message": "Login successful",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "Bearer",
                    "expires_in": Config.JWT_EXPIRY,
                    "user": jsonable_encoder(user),
                },
            },
            status_code=status.HTTP_200_OK,
        )

    async def refresh(self, user: dict, session: AsyncSession) -> dict:
        expiry_timestamp = user["exp"]

        if datetime.fromtimestamp(expiry_timestamp) < datetime.now():
            raise InvalidToken

        access_token = generate_token(
            data=user["user"],
        )

        return JSONResponse(
            content={
                "success": True,
                "message": "Token refreshed",
                "data": {
                    "access_token": access_token,
                    "token_type": "Bearer",
                    "expires_in": Config.JWT_EXPIRY,
                },
            },
            status_code=status.HTTP_200_OK,
        )

    async def last_logged_in(self, email: str, session: AsyncSession) -> datetime:
        now = datetime.now()
        async with session.begin():
            q = (
                select(Auth)
                .where(Auth.email == email)
            )
            result = await session.execute(q)
            response = result.scalars().first()

            if response is None:
                raise UserNotFound

            response.last_logged_in = now

            session.add(response)
            await session.commit()

        return now

    async def user_exists(self, email: str, session: AsyncSession) -> dict:
        async with session.begin():
            q = (
                select(
                    Auth.id,
                    Auth.name,
                    Auth.email,
                    Auth.password,
                    Role.id.label("role_id"),
                    Role.name.label("role"),
                    Auth.active,
                    Auth.last_logged_in
                )
                .select_from(Auth)
                .join(UserRole, UserRole.user_id == Auth.id)
                .join(Role, UserRole.role_id == Role.id)
                .where(Auth.email == email)
            )
            result = await session.execute(q)
            response = result.first()

            if response is None:    
                raise UserNotFound
        
        return AuthSchema(
            id=response.id,
            name=response.name,
            email=response.email,
            password=response.password,
            role_id=response.role_id,
            role=response.role,
            active=response.active,
            last_logged_in=response.last_logged_in
        )

    async def is_active(self, email: str, session: AsyncSession) -> bool:
        async with session.begin():
            q = (
                select(Auth)
                .where(Auth.email == email)
            )
            result = await session.execute(q)
            response = result.scalars().first()

            if response is None:
                raise UserNotFound

        return response.active

    async def me(self, user: dict, session: AsyncSession) -> dict:
        user_id = user["user"]["id"]
        async with session.begin():
            q = (
                select(
                    Auth.id,
                    Auth.name,
                    Auth.email,
                    Role.id.label("role_id"),
                    Role.name.label("role"),
                    Auth.active,
                    Auth.last_logged_in
                )
                .select_from(Auth)
                .join(UserRole, UserRole.user_id == Auth.id)
                .join(Role, UserRole.role_id == Role.id)
                .where(Auth.id == user_id)
            )
            result = await session.execute(q)
            response = result.first()

            if response is None:
                raise UserNotFound

        return AuthSchema(
            id=response.id,
            name=response.name,
            email=response.email,
            password="xxxxxxxx",
            role_id=response.role_id,
            role=response.role,
            active=response.active,
            last_logged_in=response.last_logged_in
        )

    async def switch(self, user: dict, request: SwitchAccountRequestSchema, session: AsyncSession) -> dict:
        jti = user["jti"]

        await redisDB.add_jti_to_blocklist(jti)

        q = (
            select(
                Auth.id,
                Auth.name,
                Auth.email,
                Role.id.label("role_id"),
                Role.name.label("role"),
                Auth.active,
                Auth.last_logged_in
            )
            .select_from(Auth)
            .join(UserRole, UserRole.user_id == Auth.id)
            .join(Role, UserRole.role_id == Role.id)
            .where(Auth.email == request.email) 
        )
        result = await session.execute(q)
        response = result.first()

        if response is None:
            raise UserNotFound
        

        user = {
            "id": response.id,
            "name": response.name,
            "email": response.email,
            "role_id": response.role_id,
            "role": response.role,
            "active": response.active,
            "last_logged_in": response.last_logged_in
        }

        access_token = generate_token(data=jsonable_encoder(user))

        return JSONResponse(
            content={
                "success": True,
                "message": "Account switched successfully",
                "data": {
                    "access_token": access_token,
                    "token_type": "Bearer",
                    "expires_in": Config.JWT_EXPIRY,
                    "user": jsonable_encoder(user),
                },
            },
            status_code=status.HTTP_200_OK,
        )

    async def change_password(self, user: dict, request: ChangePasswordRequestSchema, session: AsyncSession) -> dict:
        q = (
            select(Auth)
            .where(Auth.id == user["user"]["id"])
        )
        result = await session.execute(q)
        user = result.scalars().first()

        password = verify_password(request.old_password, user.password)
        if not password:
            raise InvalidCredentials

        # confirm new password
        if request.new_password != request.confirm_password:
            raise InvalidConfirmPassword
        
        user.password = password_hash(request.new_password)

        session.add(user)
        await session.commit()

        return JSONResponse(
            content={"success": True, "message": "Password changed successfully"},
            status_code=status.HTTP_200_OK,
        )

    async def register(self, request: RegisterRequestSchema, session: AsyncSession):
        user = await self.user_exists(request.email, session)
        if user:
            raise UserAlreadyExists
        body = Auth(**request.dict())
        body.password = password_hash(request.password)
        async with session.begin():
            session.add(body)
            await session.commit()

        return body

    async def logout(self, user: str, session: AsyncSession) -> dict:
        jti = user["jti"]

        await redisDB.add_jti_to_blocklist(jti)

        return JSONResponse(
            content={"success": True, "message": "Logout successful"},
            status_code=status.HTTP_200_OK,
        )
