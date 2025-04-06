# src/modules/logs/actions/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .schemas import ActionRequestSchema
from .models import Action
from src.modules.logs.audit_logs.models import AuditLog
from sqlmodel import select, desc, cast, String
from fastapi import status, Request
from typing import Optional
from sqlalchemy.orm import joinedload
from src.utils.logging import Logging, ActivityLog
from src.utils.actions import ActionType
from sqlalchemy import func
from src.utils.helper import DuplicateChecker

class ActionService:
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
        # Checking if the record is trashed (deleted)
        trashed = await AuditLog().is_trashed(Action)

        # Build the query for fetching data
        q = (
            select(Action)
            .select_from(Action)
            # .outerjoin(AuditLog, AuditLog.record_id == cast(Action.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(Action.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(Action.audit_logs),
                joinedload(Action.audit_logs).joinedload(AuditLog.user),
                joinedload(Action.audit_logs).joinedload(AuditLog.action),
            )
            .filter(~trashed)  # Exclude trashed data
            .order_by(
                desc(Action.id)
            )  # Order by Action.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = (
            select(func.count(Action.id))
            .select_from(Action)
            .filter(~trashed)
        )
        if keywords:
            count_query = count_query.filter(Action.name.ilike(f"{keywords}"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (
            total_count + limit - 1
        ) // limit  # This is the ceiling of total_count / limit

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
    ) -> Optional[Action]:
        trashed = await AuditLog().is_trashed(Action)
        q = (
            select(Action)
            .options(
                joinedload(Action.audit_logs),
                joinedload(Action.audit_logs).joinedload(AuditLog.user),
                joinedload(Action.audit_logs).joinedload(AuditLog.action),
            )
            .where(Action.id == id)
            .filter(~trashed)
        )
        action = await session.execute(q)
        response = action.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Action not found"
            )
        return response

    async def create(
        self, request: Request, body: ActionRequestSchema, session: AsyncSession
    ) -> dict:
        # Check if the record already exists
        checker = DuplicateChecker(Action, session)
        await checker.check({"name": body.name}) # Change the field name if necessary
        try:
            body = Action(**body.dict())
            body.name = body.name.upper()
            session.add(body)
            await session.commit()

            await self.activity_log(
                request=request,
                body={
                    "action_id": await self.action_type("CREATE", session),
                    "record_id": body.id,
                    "model_name": Action.__tablename__,
                },
                session=session,
            )
            return body
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def update(
        self,
        id: int,
        request: Request,
        body: ActionRequestSchema,
        session: AsyncSession,
    ) -> dict:# Check if the record already exists
        checker = DuplicateChecker(Action, session)
        await checker.check({"name": body.name}) # Change the field name if necessary
        response = await self.find(id, request, session)
        try:
            if response:
                for key, value in body.dict().items():
                    # value name should be uppercase
                    if key == "name":
                        value = value.upper()
                        
                    setattr(response, key, value)
                await session.commit()

            await self.activity_log(
                request=request,
                body={
                    "action_id": await self.action_type("UPDATE", session),
                    "record_id": id,
                    "model_name": Action.__tablename__,
                },
                session=session,
            )

            return response
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def destroy(self, id: int, request: Request, session: AsyncSession) -> dict:
        response = await self.find(id, request, session)

        if await Action().is_used(id, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Cannot delete this data because it is used in other transactions"
            )

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("DELETE", session),
                "record_id": id,
                "model_name": Action.__tablename__,
            },
            session=session,
        )

        return response

    async def trash(
        self,
        request: Request,
        session: AsyncSession,
        keywords: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> dict:
        # Checking if the record is trashed (deleted)
        trashed = await AuditLog().is_trashed(Action)

        # Build the query for fetching data
        q = (
            select(Action)
            .select_from(Action)
            .outerjoin(AuditLog, AuditLog.record_id == cast(Action.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(Action.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(Action.audit_logs),
                joinedload(Action.audit_logs).joinedload(AuditLog.user),
                joinedload(Action.audit_logs).joinedload(AuditLog.action),
            )
            .filter(trashed)  # Just trashed data
            .order_by(
                desc(Action.id)
            )  # Order by Action.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = (
            select(func.count(Action.id))
            .select_from(Action)
            .filter(trashed)
        )
        if keywords:
            count_query = count_query.filter(Action.name.ilike(f"{keywords}"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (
            total_count + limit - 1
        ) // limit  # This is the ceiling of total_count / limit

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

    async def restore(self, id: int, request: Request, session: AsyncSession) -> dict:
        q = select(Action).where(Action.id == id)
        action = await session.execute(q)
        response = action.scalars().first()

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Action not found"
            )

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("RESTORE", session),
                "record_id": id,
                "model_name": Action.__tablename__,
            },
            session=session,
        )

        return response

    async def colors(self) -> dict:
        colours = [
            {"id": 1, "name": "red"},
            {"id": 2, "name": "orange"},
            {"id": 3, "name": "amber"},
            {"id": 4, "name": "yellow"},
            {"id": 5, "name": "lime"},
            {"id": 6, "name": "green"},
            {"id": 7, "name": "emerald"},
            {"id": 8, "name": "teal"},
            {"id": 9, "name": "cyan"},
            {"id": 10, "name": "sky"},
            {"id": 11, "name": "blue"},
            {"id": 12, "name": "indigo"},
            {"id": 13, "name": "violet"},
            {"id": 14, "name": "purple"},
            {"id": 15, "name": "fuchsia"},
            {"id": 16, "name": "pink"},
            {"id": 17, "name": "rose"},
            {"id": 18, "name": "slate"},
            {"id": 19, "name": "gray"},
            {"id": 20, "name": "zinc"},
            {"id": 21, "name": "neutral"},
            {"id": 22, "name": "stone"}
        ]

        return colours
