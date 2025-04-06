# src/modules/authentications/roles/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from fastapi import APIRouter, status, Depends, Request, Query
from fastapi.exceptions import HTTPException
from .schemas import (
    RoleRequestSchema,
    RoleSchema,
    RoleResponseSchema,
    GivePermissionToRoleSchema,
    SelectRoleSchema
)
from src.modules.authentications.roles.models import Role
from .services import RoleService
from src.databases import db
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.utils.dependency import (
    AccessTokenBearer,
    AccessControlBearer,
)

router = APIRouter(
    dependencies=[
        Depends(AccessTokenBearer()),
    ],
)

service = RoleService()
session = db.session


@router.get("/", response_model=RoleResponseSchema, status_code=status.HTTP_200_OK)
async def index(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(AccessControlBearer(permissions=["manage:roles", "view:roles"])),
):
    return await service.all(request, session, keywords, skip, limit)


@router.get("/{id}", response_model=RoleSchema, status_code=status.HTTP_200_OK)
async def show(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:roles", "show:roles"])),
):
    return await service.find(id, request, session)

@router.get("/select/all", response_model=List[SelectRoleSchema], status_code=status.HTTP_200_OK)
async def select_all(
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:roles", "select:roles"])),
):
    return await service.select(request, session)

@router.post("/", response_model=Role, status_code=status.HTTP_201_CREATED)
async def store(
    request: Request,
    body: RoleRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:roles", "create:roles"])
    ),
):
    return await service.create(request, body, session)


@router.put("/{id}", response_model=Role, status_code=status.HTTP_200_OK)
async def update(
    id: int,
    request: Request,
    body: RoleRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:roles", "update:roles"])
    ),
):
    return await service.update(id, request, body, session)


@router.patch(
    "/give-permissions", status_code=status.HTTP_200_OK
)
async def give_permission(
    request: Request,
    body: GivePermissionToRoleSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:roles", "grant:role-permissions"])
    ),
):
    return await service.give_permission_to_role(request, body, session)

@router.patch(
    "/revoke-permissions", status_code=status.HTTP_200_OK
)
async def revoke_permission(
    request: Request,
    body: GivePermissionToRoleSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:roles", "revoke:role-permissions"])
    ),
):
    return await service.revoke_permission_to_role(request, body, session)

@router.delete("/{id}", response_model=Role, status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:roles", "delete:roles"])
    ),
):
    return await service.destroy(id, request, session)

@router.get("/trash/all", response_model=RoleResponseSchema, status_code=status.HTTP_200_OK)
async def trash(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(AccessControlBearer(permissions=["manage:roles", "trash:roles"])),
):
    return await service.trash(request, session, keywords, skip, limit)

@router.patch("/{id}", response_model=Role, status_code=status.HTTP_200_OK)
async def patch(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:roles", "restore:roles"])
    ),
):
    return await service.restore(id, request, session)
