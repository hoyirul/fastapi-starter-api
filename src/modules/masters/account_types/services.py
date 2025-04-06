# src/modules/masters/account_types/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .schemas import AccountTypeRequestSchema, SelectAccountTypeSchema
from .models import AccountType
from src.modules.logs.audit_logs.models import AuditLog
from sqlmodel import select, desc, cast, String
from fastapi import status, Request
from typing import Optional
from sqlalchemy.orm import joinedload
from src.utils.logging import Logging, ActivityLog
from src.utils.actions import ActionType
from sqlalchemy import func
from src.utils.helper import DuplicateChecker

class AccountTypeService:
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
        trashed = await AuditLog().is_trashed(AccountType)

        # Build the query for fetching data
        q = (
            select(AccountType)
            .select_from(AccountType)
            # .outerjoin(AuditLog, AuditLog.record_id == cast(AccountType.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(AccountType.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(AccountType.audit_logs),
                joinedload(AccountType.audit_logs).joinedload(AuditLog.user),
                joinedload(AccountType.audit_logs).joinedload(AuditLog.action),
            )
            .filter(~trashed)  # Exclude trashed data
            .order_by(desc(AccountType.id))  # Order by AccountType.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = (
            select(func.count(AccountType.id)).select_from(AccountType).filter(~trashed)
        )
        if keywords:
            count_query = count_query.filter(AccountType.name.ilike(f"{keywords}"))
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
    ) -> Optional[AccountType]:
        trashed = await AuditLog().is_trashed(AccountType)
        q = (
            select(AccountType)
            .options(
                joinedload(AccountType.audit_logs),
                joinedload(AccountType.audit_logs).joinedload(AuditLog.user),
                joinedload(AccountType.audit_logs).joinedload(AuditLog.action),
            )
            .where(AccountType.id == id)
            .filter(~trashed)
        )
        accounttype = await session.execute(q)
        self.logger.log("debug", f"AccountType: {accounttype}")
        response = accounttype.scalars().first()
        self.logger.log("debug", f"Response: {response}")
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="AccountType not found"
            )
        return response

    async def select(self, request: Request, session: AsyncSession) -> list:
        trashed = await AuditLog().is_trashed(AccountType)
        q = select(AccountType).filter(~trashed).order_by(AccountType.id)
        result = await session.execute(q)
        response = result.scalars().all()

        return response

    async def create(
        self, request: Request, body: AccountTypeRequestSchema, session: AsyncSession
    ) -> dict:
        # Check if the record already exists
        checker = DuplicateChecker(AccountType, session)
        await checker.check({"name": body.name}) # Change the field name if necessary
        try:
            body = AccountType(**body.dict())
            body.name = body.name.title()
            session.add(body)
            await session.commit()

            await self.activity_log(
                request=request,
                body={
                    "action_id": await self.action_type("CREATE", session),
                    "record_id": body.id,
                    "model_name": AccountType.__tablename__,
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
        body: AccountTypeRequestSchema,
        session: AsyncSession,
    ) -> dict:
        # Check if the record already exists
        checker = DuplicateChecker(AccountType, session)
        await checker.check({"name": body.name}) # Change the field name if necessary

        response = await self.find(id, request, session)
        try: 
            body.name = body.name.title()
            for key, value in body.dict().items():
                setattr(response, key, value)
            await session.commit()

            await self.activity_log(
                request=request,
                body={
                    "action_id": await self.action_type("UPDATE", session),
                    "record_id": id,
                    "model_name": AccountType.__tablename__,
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

        if await AccountType().is_used(id, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete this data because it is used in other transactions"
            )

        # await session.delete(response) # This hard delete the record, you can change it to soft delete with:
        # await session.commit()

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("DELETE", session),
                "record_id": id,
                "model_name": AccountType.__tablename__,
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
        trashed = await AuditLog().is_trashed(AccountType)

        # Build the query for fetching data
        q = (
            select(AccountType)
            .select_from(AccountType)
            .outerjoin(AuditLog, AuditLog.record_id == cast(AccountType.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(AccountType.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(AccountType.audit_logs),
                joinedload(AccountType.audit_logs).joinedload(AuditLog.user),
                joinedload(AccountType.audit_logs).joinedload(AuditLog.action),
            )
            .filter(trashed)  # Exclude trashed data
            .order_by(desc(AccountType.id))  # Order by AccountType.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = (
            select(func.count(AccountType.id)).select_from(AccountType).filter(trashed)
        )
        if keywords:
            count_query = count_query.filter(AccountType.name.ilike(f"{keywords}"))
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
        q = select(AccountType).where(AccountType.id == id)
        accounttype = await session.execute(q)
        response = accounttype.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="AccountType not found"
            )

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("RESTORE", session),
                "record_id": id,
                "model_name": AccountType.__tablename__,
            },
            session=session,
        )

        return response
