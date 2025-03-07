# src/modules/authentications/users/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from fastapi import APIRouter, status, Depends, Request, Query
from fastapi.exceptions import HTTPException
from .schemas import (
    UserRequestSchema, 
    AssignRoleSchema, 
    GivePermissionToUserSchema,
    SelectUserSchema,
    UserUpdateRequestSchema
)
from src.modules.authentications.users.models import User
from .services import UserService
from .schemas import UserSchema, UserResponseSchema
from src.databases import db
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.utils.dependency import AccessTokenBearer, AccessControlBearer

router = APIRouter(
    dependencies=[Depends(AccessTokenBearer())],
)

service = UserService()
session = db.session


@router.get("/", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def index(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(AccessControlBearer(permissions=["manage:users", "view:users"])),
):
    return await service.all(request, session, keywords, skip, limit)

@router.get("/select/all", response_model=List[SelectUserSchema], status_code=status.HTTP_200_OK)
async def select_all(
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:users", "select:users"])),
):
    return await service.select(request, session)

@router.get("/{id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def show(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:users", "show:users"])),
):
    return await service.find(id, request, session)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def store(
    request: Request,
    body: UserRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:users", "create:users"])
    ),
):
    return await service.create(request, body, session)


@router.put("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def update(
    id: int,
    request: Request,
    body: UserUpdateRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:users", "update:users"])
    ),
):
    return await service.update(id, request, body, session)


@router.patch("/assign-role", status_code=status.HTTP_200_OK)
async def assign_role(
    request: Request,
    body: AssignRoleSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:users", "assign:roles"])
    ),
):
    return await service.assign_role(request, body, session)

@router.patch(
    "/revoke-role", status_code=status.HTTP_200_OK
)
async def revoke_role(
    request: Request,
    body: AssignRoleSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:users", "revoke:roles"])
    ),
):
    return await service.revoke_role(request, body, session)

@router.patch(
    "/give-permissions", status_code=status.HTTP_200_OK
)
async def give_permission(
    request: Request,
    body: GivePermissionToUserSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:users", "grant:user-permissions"])
    ),
):
    return await service.give_permission_to_user(request, body, session)

@router.patch(
    "/revoke-permissions", status_code=status.HTTP_200_OK
)
async def revoke_permission(
    request: Request,
    body: GivePermissionToUserSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:users", "revoke:user-permissions"])
    ),
):
    return await service.revoke_permission_to_user(request, body, session)

@router.patch("/{id}/inactive", response_model=User, status_code=status.HTTP_200_OK)
async def inactive(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:users", "inactive:users"])
    ),
):
    return await service.inactive(id, request, session)


@router.patch("/{id}/active", response_model=User, status_code=status.HTTP_200_OK)
async def active(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:users", "active:users"])
    ),
):
    return await service.active(id, request, session)
