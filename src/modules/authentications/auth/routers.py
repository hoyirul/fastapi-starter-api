# src/modules/authentications/auth/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from fastapi import APIRouter, status, Depends, Request
from fastapi.exceptions import HTTPException
from .schemas import (
    LoginRequestSchema, 
    RegisterRequestSchema, 
    AuthSchema, 
    SwitchAccountRequestSchema,
    ChangePasswordRequestSchema
)
from .models import Auth
from .services import AuthService
from src.databases import db
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.utils.security import verify_password, generate_token
from src.configs import Config
from src.utils.dependency import (
    AccessTokenBearer, 
    RefreshTokenBearer,
    AccessControlBearer
)

router = APIRouter()

service = AuthService()
session = db.session


@router.post("/login", response_model=AuthSchema, status_code=status.HTTP_200_OK)
async def login(request: Request, body: LoginRequestSchema, session: AsyncSession = Depends(session)):
    return await service.login(request, body, session)


@router.post("/register", response_model=Auth, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    body: RegisterRequestSchema, 
    session: AsyncSession = Depends(session)
):
    return await service.register(request, body, session)


@router.get("/me", response_model=AuthSchema, status_code=status.HTTP_200_OK, dependencies=[Depends(AccessTokenBearer())])
async def me(
    request: Request,
    user: dict = Depends(AccessTokenBearer()), 
    session: AsyncSession = Depends(session)
):
    return await service.me(request, user, session)

# switch account
@router.post(
    "/switch",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AccessTokenBearer())],
)
async def switch(
    request: Request,
    user: dict = Depends(AccessTokenBearer()),
    body: SwitchAccountRequestSchema = None,
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:auth", "switch:auth"]))
):
    return await service.switch(request, user, body, session)

# change password
@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AccessTokenBearer())],
)
async def change_password(
    request: Request,
    user: dict = Depends(AccessTokenBearer()),
    body: ChangePasswordRequestSchema = None,
    session: AsyncSession = Depends(session)
):
    return await service.change_password(request, user, body, session)

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AccessTokenBearer())],
)
async def logout(
    request: Request,
    user: dict = Depends(AccessTokenBearer()), 
    session: AsyncSession = Depends(session)
):
    return await service.logout(request, user, session)

# refresh token
@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RefreshTokenBearer())],
)
async def refresh(
    request: Request,
    user: dict = Depends(RefreshTokenBearer()), 
    session: AsyncSession = Depends(session)
):
    return await service.refresh(request, user, session)
