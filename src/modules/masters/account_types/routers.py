# src/modules/masters/account_types/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from fastapi import APIRouter, status, Depends, Request, Query
from fastapi.exceptions import HTTPException
from .schemas import (
    AccountTypeRequestSchema,
    AccountTypeSchema,
    AccountTypeResponseSchema,
    SelectAccountTypeSchema
)
from .models import AccountType
from .services import AccountTypeService
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

service = AccountTypeService()
session = db.session


@router.get(
    "/", response_model=AccountTypeResponseSchema, status_code=status.HTTP_200_OK
)
async def index(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:account-types", "view:account-types"])
    ),
):
    return await service.all(request, session, keywords, skip, limit)


@router.get("/{id}", response_model=AccountTypeSchema, status_code=status.HTTP_200_OK)
async def show(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:account-types", "show:account-types"])
    ),
):
    return await service.find(id, request, session)

@router.get("/select/all", response_model=List[SelectAccountTypeSchema], status_code=status.HTTP_200_OK)
async def select_all(
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:account-types", "select:account-types"])
    ),
):
    return await service.select(request, session)

@router.post("/", response_model=AccountType, status_code=status.HTTP_201_CREATED)
async def store(
    request: Request,
    body: AccountTypeRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(
            permissions=["manage:account-types", "create:account-types"]
        )
    ),
):
    return await service.create(request, body, session)


@router.put("/{id}", response_model=AccountType, status_code=status.HTTP_200_OK)
async def update(
    id: int,
    request: Request,
    body: AccountTypeRequestSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(
            permissions=["manage:account-types", "update:account-types"]
        )
    ),
):
    return await service.update(id, request, body, session)


@router.delete("/{id}", response_model=AccountType, status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(
            permissions=["manage:account-types", "delete:account-types"]
        )
    ),
):
    return await service.destroy(id, request, session)

@router.get(
    "/trash/all", response_model=AccountTypeResponseSchema, status_code=status.HTTP_200_OK
)
async def trash(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:account-types", "trash:account-types"])
    ),
):
    return await service.trash(request, session, keywords, skip, limit)

@router.patch("/{id}", response_model=AccountType, status_code=status.HTTP_200_OK)
async def patch(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(
            permissions=["manage:account-types", "restore:account-types"]
        )
    ),
):
    return await service.restore(id, request, session)
