# src/modules/authentications/auth/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from fastapi import status, Request
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
from src.utils.logging import Logging, ActivityLog
from src.utils.actions import ActionType
import re

redisDB = RedisDB()

# Password regex
# Minimum 8 characters, at least one uppercase letter, one lowercase letter, one number and one special character
password_regex = re.compile(
    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/-]).{8,}$'
)

MAX_FAILED_ATTEMPTS = 3

class AuthService:
    def __init__(self):
        self.logger = Logging(level="DEBUG")
        self.activity_log = ActivityLog(level="DEBUG")
        self.action_type = ActionType()

    async def login(self, request: Request, body: LoginRequestSchema, session: AsyncSession) -> dict:
        user = await self.user_exists(body.email, session)

        if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been locked. Please contact the administrator or IT support."
            )
        
        if not await self.is_active(body.email, session):
            raise UserIsInactive

        password = verify_password(body.password, user.password)
        if not password:
            user.failed_login_attempts += 1
            await self.failed_login(body.email, user.failed_login_attempts, session)

            if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                user.active = False
                await session.commit()
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Your remaining login attempts are {MAX_FAILED_ATTEMPTS - user.failed_login_attempts}. If you fail to login {MAX_FAILED_ATTEMPTS} times, your account will be locked." if user.failed_login_attempts < MAX_FAILED_ATTEMPTS else "Your account has been locked. Please contact the administrator or IT support."
            )

        user.failed_login_attempts = 0
        await session.commit()

        access_token = generate_token(data=jsonable_encoder(user))
        refresh_token = generate_token(
            data=jsonable_encoder(user),
            expiry=timedelta(seconds=Config.JWT_REFRESH_EXPIRY),
            refresh=True,
        )

        await self.activity_log(
            request=request,
            body={
                "user_id": user.id,
                "action_id": await self.action_type("LOGIN", session),
                "record_id": user.id,
                "model_name": Auth.__tablename__,
                "ip_address": request.client.host,
                "notes": f"User {user.email} has logged in"
            },
            session=session
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

    async def refresh(self, request: Request, user: dict, session: AsyncSession) -> dict:
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

    async def failed_login(self, email: str, fails: int, session: AsyncSession) -> int:
        async with session.begin():
            q = (
                select(Auth)
                .where(Auth.email == email)
            )
            result = await session.execute(q)
            response = result.scalars().first()

            if response is None:
                raise UserNotFound

            response.failed_login_attempts = fails

            if response.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                response.active = False

            session.add(response)
            await session.commit()

        return response.failed_login_attempts

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
                    Auth.last_logged_in,
                    Auth.failed_login_attempts
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
            last_logged_in=response.last_logged_in,
            failed_login_attempts=response.failed_login_attempts
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

    async def me(self, request: Request, user: dict, session: AsyncSession) -> dict:
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
                    Auth.last_logged_in,
                    Auth.failed_login_attempts
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
            last_logged_in=response.last_logged_in,
            failed_login_attempts=response.failed_login_attempts
        )

    async def switch(self, request: Request, user: dict, body: SwitchAccountRequestSchema, session: AsyncSession) -> dict:
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
            .where(Auth.email == body.email) 
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

    async def change_password(self, request: Request, user: dict, body: ChangePasswordRequestSchema, session: AsyncSession) -> dict:
        q = (
            select(Auth)
            .where(Auth.id == user["user"]["id"])
        )
        result = await session.execute(q)
        user = result.scalars().first()

        password = verify_password(body.old_password, user.password)
        if not password:
            raise InvalidCredentials

        # Confirm new password
        if body.new_password != body.confirm_password:
            raise InvalidConfirmPassword

        # Validate password
        if not password_regex.match(body.new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        
        try:
            # If all is well, update the password
            user.password = password_hash(body.new_password)

            session.add(user)
            await session.commit()

            await self.activity_log(
                request=request,
                body={
                    "user_id": user.id,
                    "action_id": await self.action_type("UPDATE", session),
                    "record_id": user.id,
                    "model_name": Auth.__tablename__,
                    "ip_address": request.client.host,
                    "notes": f"User {user.email} has changed their password"
                },
                session=session
            )

            return JSONResponse(
                content={"success": True, "message": "Password changed successfully"},
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def forgot_password(self, request: Request, body: dict, session: AsyncSession) -> dict:
        pass

    async def register(self, request: Request, body: RegisterRequestSchema, session: AsyncSession):
        from src.modules.authentications.users.models import UserRole
        q = (
            select(Auth)
            .where(Auth.email == body.email)
        )
        result = await session.execute(q)
        user = result.scalars().first()

        if user:
            raise UserAlreadyExists
        try:
            body = Auth(**body.dict())
            body.password = password_hash(body.password)
            session.add(body)
            await session.commit()

            # add user role
            q = (
                select(Role)
                .where(Role.name == "User")
            )
            result = await session.execute(q)
            role = result.scalars().first()

            user_role = UserRole(user_id=body.id, role_id=role.id)
            session.add(user_role)
            await session.commit()

            return body
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def logout(self, request: Request, user: str, session: AsyncSession) -> dict:
        jti = user["jti"]

        await self.activity_log(
            request=request,
            body={
                "user_id": user["user"]["id"],
                "action_id": await self.action_type("LOGOUT", session),
                "record_id": user["user"]["id"],
                "model_name": Auth.__tablename__,
                "ip_address": request.client.host,
                "notes": f"User {user['user']['email']} has logged out"
            },
            session=session
        )

        await redisDB.add_jti_to_blocklist(jti)


        return JSONResponse(
            content={"success": True, "message": "Logout successful"},
            status_code=status.HTTP_200_OK,
        )
