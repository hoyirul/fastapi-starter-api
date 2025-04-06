# src/modules/logs/audit_logs/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .models import AuditLog
from sqlmodel import select, desc, cast, String
from fastapi import status, Request
from typing import Optional
from sqlalchemy.orm import joinedload
from src.utils.logging import Logging, ActivityLog
from src.utils.actions import ActionType
from sqlalchemy import func


class AuditLogService:
    # you can delete the function below if you don't need it
    def __init__(self):
        self.logger = Logging(level="DEBUG")
        self.activity_log = ActivityLog(level="DEBUG")
        self.action_type = ActionType()

    async def all(
        self,
        request: Request,
        session: AsyncSession,
        keywords: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> dict:
        # Query dasar untuk audit_logs
        q = select(AuditLog).options(
            joinedload(AuditLog.user),  # Mengambil relasi 'user'
            joinedload(AuditLog.action),  # Mengambil relasi 'action'
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(AuditLog.model_name.ilike(f"%{keywords}%"))

        q = (
            q.order_by(desc(AuditLog.id))  # Order by AuditLog.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data with pagination
        result = await session.execute(q)
        response = result.scalars().all()

        # Count the total number of records without pagination
        count_query = select(func.count(AuditLog.id))
        if keywords:
            count_query = count_query.filter(AuditLog.model_name.ilike(f"%{keywords}%"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (total_count + limit - 1) // limit  # Ceiling of total_count / limit

        # Calculate the current page based on skip and limit
        current_page = skip // limit + 1 if total_count > 0 else 0

        # Return the data along with pagination information
        return {
            "current_page": current_page,
            "total_count": total_count,
            "per_page": limit,
            "total_pages": total_pages,
            "data": response,
        }

    async def own_activities(
        self,
        request: Request,
        session: AsyncSession,
        keywords: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> dict:
        # Query dasar untuk audit_logs
        q = select(AuditLog).options(
            joinedload(AuditLog.user),  # Mengambil relasi 'user'
            joinedload(AuditLog.action),  # Mengambil relasi 'action'
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(AuditLog.model_name.ilike(f"%{keywords}%"))

        q = (
            q.order_by(desc(AuditLog.id))  # Order by AuditLog.id descending
            .filter(AuditLog.user_id == request.state.authorize['user']['id'])  # Filter by user_id
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data with pagination
        result = await session.execute(q)
        response = result.scalars().all()

        # Count the total number of records without pagination
        count_query = select(func.count(AuditLog.id))
        if keywords:
            count_query = count_query.filter(AuditLog.model_name.ilike(f"%{keywords}%"))
        count_query = count_query.filter(AuditLog.user_id == request.state.authorize['user']['id'])
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (total_count + limit - 1) // limit  # Ceiling of total_count / limit

        # Calculate the current page based on skip and limit
        current_page = skip // limit + 1 if total_count > 0 else 0

        # Return the data along with pagination information
        return {
            "current_page": current_page,
            "total_count": total_count,
            "per_page": limit,
            "total_pages": total_pages,
            "data": response,
        }

    async def find(
        self, id: int, request: Request, session: AsyncSession
    ) -> Optional[AuditLog]:
        q = select(AuditLog).options(
            joinedload(AuditLog.user),  # Mengambil relasi 'user'
            joinedload(AuditLog.action),  # Mengambil relasi 'action'
        ).filter(AuditLog.id == id)

        result = await session.execute(q)
        response = result.scalars().first()

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not found",
            )

        return response
    
    async def find_own_log(
        self, id: int, request: Request, session: AsyncSession
    ) -> Optional[AuditLog]:
        q = select(AuditLog).options(
            joinedload(AuditLog.user),  # Mengambil relasi 'user'
            joinedload(AuditLog.action),  # Mengambil relasi 'action'
        ).filter(AuditLog.id == id).filter(AuditLog.user_id == request.state.authorize['user']['id'])

        result = await session.execute(q)
        response = result.scalars().first()

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not found",
            )

        return response