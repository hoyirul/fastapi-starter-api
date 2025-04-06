# src/modules/logs/audit_logs/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from fastapi import APIRouter, status, Depends, Request, Query
from fastapi.exceptions import HTTPException
from .schemas import AuditLogResponseSchema
from .models import AuditLog
from .services import AuditLogService
from .schemas import AuditLogSchema
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

service = AuditLogService()
session = db.session

@router.get(
    "/", response_model=AuditLogResponseSchema, status_code=status.HTTP_200_OK
)
async def index(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:audit-logs", "view:audit-logs"])
    ),
):
    return await service.all(request, session, keywords, skip, limit)

@router.get(
    "/own/activities", response_model=AuditLogResponseSchema, status_code=status.HTTP_200_OK
)
async def index(
    request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    return await service.own_activities(request, session, keywords, skip, limit)

@router.get("/own/{id}/activities", response_model=AuditLogSchema, status_code=status.HTTP_200_OK)
async def show(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
):
    return await service.find_own_log(id, request, session)

@router.get("/{id}", response_model=AuditLogSchema, status_code=status.HTTP_200_OK)
async def show(
    id: int,
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:audit-logs", "show:audit-logs"])
    ),
):
    return await service.find(id, request, session)