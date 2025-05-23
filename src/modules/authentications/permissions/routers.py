# src/modules/authentications/permissions/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from fastapi import APIRouter, status, Depends, Request, Query
from fastapi.exceptions import HTTPException
from .schemas import (
    PermissionRequestSchema, 
    PermissionSchema, 
    PermissionResponseSchema,
    SelectPermissionSchema,
    HasPermissionRequestSchema,
)
from src.modules.authentications.permissions.models import Permission
from .services import PermissionService
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

service = PermissionService()
session = db.session


@router.get(
    "/", response_model=PermissionResponseSchema, status_code=status.HTTP_200_OK
)
async def index(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:permissions", "view:permissions"])
    ),
):
    return await service.all(request, session, keywords, skip, limit)


@router.get("/{id}", response_model=PermissionSchema, status_code=status.HTTP_200_OK)
async def show(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:permissions", "show:permissions"])
    ),
):
    return await service.find(id, request, session)

@router.post("/authorize", status_code=status.HTTP_200_OK)
async def authorize(
    body: HasPermissionRequestSchema,
    request: Request,
    session: AsyncSession = Depends(session),
):
    return await service.authorize(body, request, session)

@router.get("/select/all", response_model=List[SelectPermissionSchema], status_code=status.HTTP_200_OK)
async def select_all(
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:permissions", "select:permissions"])
    ),
):
    return await service.select(request, session)

@router.post("/", response_model=Permission, status_code=status.HTTP_201_CREATED)
async def store(
    request: Request,
    body: PermissionRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:permissions", "create:permissions"])
    ),
):
    return await service.create(request, body, session)


@router.put("/{id}", response_model=Permission, status_code=status.HTTP_200_OK)
async def update(
    id: int,
    request: Request,
    body: PermissionRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:permissions", "update:permissions"])
    ),
):
    return await service.update(id, request, body, session)


@router.delete("/{id}", response_model=Permission, status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:permissions", "delete:permissions"])
    ),
):
    return await service.destroy(id, request, session)

@router.get(
    "/trash/all", response_model=PermissionResponseSchema, status_code=status.HTTP_200_OK
)
async def trash(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:permissions", "trash:permissions"])
    ),
):
    return await service.trash(request, session, keywords, skip, limit)

@router.patch("/{id}", response_model=Permission, status_code=status.HTTP_200_OK)
async def patch(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:permissions", "restore:permissions"])
    ),
):
    return await service.restore(id, request, session)