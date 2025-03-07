# src/modules/logs/actions/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from fastapi import APIRouter, status, Depends, Request, Query
from fastapi.exceptions import HTTPException
from .schemas import ActionRequestSchema
from .models import Action
from .services import ActionService
from .schemas import (
    ActionResponseSchema,
    ActionSchema,
    ActionRequestSchema,
    ColorSchema
)
from src.databases import db
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.utils.dependency import (
    AccessTokenBearer,
    AccessControlBearer,
)

router = APIRouter(
    dependencies=[Depends(AccessTokenBearer())],
)

service = ActionService()
session = db.session


@router.get("/", response_model=ActionResponseSchema, status_code=status.HTTP_200_OK)
async def index(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:actions", "view:actions"])
    ),
):
    return await service.all(request, session, keywords, skip, limit)


@router.get("/{id}", response_model=ActionSchema, status_code=status.HTTP_200_OK)
async def show(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:actions", "show:actions"])
    ),
):
    return await service.find(id, request, session)


@router.post("/", response_model=Action, status_code=status.HTTP_201_CREATED)
async def store(
    request: Request,
    body: ActionRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:actions", "create:actions"])
    ),
):
    return await service.create(request, body, session)


@router.put("/{id}", response_model=Action, status_code=status.HTTP_200_OK)
async def update(
    id: int,
    request: Request,
    body: ActionRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:actions", "update:actions"])
    ),
):
    return await service.update(id, request, body, session)


@router.delete("/{id}", response_model=Action, status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:actions", "delete:actions"])
    ),
):
    return await service.destroy(id, request, session)

@router.get("/trash/all", response_model=ActionResponseSchema, status_code=status.HTTP_200_OK)
async def index(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:actions", "trash:actions"])
    ),
):
    return await service.trash(request, session, keywords, skip, limit)

@router.patch("/{id}", response_model=Action, status_code=status.HTTP_200_OK)
async def patch(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:actions", "restore:actions"])
    ),
):
    return await service.restore(id, request, session)

@router.get(
    "/colors/all",
    response_model=List[ColorSchema],
    status_code=status.HTTP_200_OK,
)
async def colors(
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:actions", "color:actions"])
    ),
):
    return await service.colors()