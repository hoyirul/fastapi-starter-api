# src/modules/authentications/permissions/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .schemas import PermissionRequestSchema, HasPermissionRequestSchema
from .models import Permission
from src.modules.logs.audit_logs.models import AuditLog
from sqlmodel import select, desc, cast, String
from fastapi import status, Request
from typing import Optional
from sqlalchemy.orm import joinedload
from src.modules.authentications.users.models import User
from src.utils.logging import Logging, ActivityLog
from src.utils.actions import ActionType
from sqlalchemy import func
from src.utils.helper import DuplicateChecker

class PermissionService:
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
        trashed = await AuditLog().is_trashed(Permission)

        # Build the query for fetching data
        q = (
            select(Permission)
            .distinct()  # This will ensure only unique Permission records are returned
            .select_from(Permission)
            .outerjoin(AuditLog, AuditLog.record_id == cast(Permission.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(Permission.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(Permission.audit_logs),
                joinedload(Permission.audit_logs).joinedload(AuditLog.user),
                joinedload(Permission.audit_logs).joinedload(AuditLog.action),
            )
            .filter(~trashed)  # Exclude trashed data
            .order_by(desc(Permission.id))  # Order by Permission.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        self.logger.log("info", f"Permission: {response}")

        # Count the total number of records without pagination
        count_query = (
            select(func.count(Permission.id)).select_from(Permission).filter(~trashed)
        )
        if keywords:
            count_query = count_query.filter(Permission.name.ilike(f"{keywords}"))
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
    ) -> Optional[Permission]:
        trashed = await AuditLog().is_trashed(Permission)
        q = (
            select(Permission)
            .options(
                joinedload(Permission.audit_logs),
                joinedload(Permission.audit_logs).joinedload(AuditLog.user),
                joinedload(Permission.audit_logs).joinedload(AuditLog.action),
            )
            .where(Permission.id == id)
            .filter(~trashed)
        )
        permission = await session.execute(q)
        response = permission.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
            )
        return response

    async def authorize(
        self, body: HasPermissionRequestSchema, request: Request, session: AsyncSession
    ) -> dict:
        from src.modules.authentications.roles.models import RolePermission
        from src.modules.authentications.users.models import UserPermission

        if request.state.authorize["user"]["role_id"] == 1:
            return {
                "authorized": True,
                "permission": "Super Admin has all permissions",
            }

        q = (
            select(RolePermission)
            .join(Permission)
            .where(Permission.name == body.name)
            .where(RolePermission.role_id == request.state.authorize["user"]["role_id"])
        )

        result = await session.execute(q)
        response = result.scalars().first()

        if response is None:
            q = (
                select(UserPermission)
                .join(Permission)
                .where(Permission.name == body.name)
                .where(UserPermission.user_id == request.state.authorize["user"]["id"])
            )
            result = await session.execute(q)
            response = result.scalars().first()

            if response is None:
                return {
                    "authorized": False,
                    "permission": None,
                }
        
        return {
            "authorized": True,
            "permission": response,
        }

    async def select(self, request: Request, session: AsyncSession) -> list:
        trashed = await AuditLog().is_trashed(Permission)
        q = select(Permission).filter(~trashed).order_by(Permission.id)
        result = await session.execute(q)
        response = result.scalars().all()
        
        return response

    async def create(
        self,
        request: Request,
        body: PermissionRequestSchema,
        session: AsyncSession,
    ) -> dict:
        # Check if the record already exists
        checker = DuplicateChecker(Permission, session)
        await checker.check({
                "name": body.name
            }) # Change the field name if necessary
        try:
            body = Permission(**body.dict())
            body.name = body.name.title()
            session.add(body)
            await session.commit()

            await self.activity_log(
                request=request,
                body={
                    "action_id": await self.action_type("CREATE", session),
                    "record_id": body.id,
                    "model_name": Permission.__tablename__,
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
        body: PermissionRequestSchema,
        session: AsyncSession,
    ) -> dict:
        # Check if the record already exists
        checker = DuplicateChecker(Permission, session)
        await checker.check({
                "name": body.name
            }) # Change the field name if necessary
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
                    "model_name": Permission.__tablename__,
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

        if await Permission().is_used(id, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete this data because it is used in other transactions"
            )
        
        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("DELETE", session),
                "record_id": id,
                "model_name": Permission.__tablename__,
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
        trashed = await AuditLog().is_trashed(Permission)

        # Build the query for fetching data
        q = (
            select(Permission)
            .distinct()  # This will ensure only unique Permission records are returned
            .select_from(Permission)
            .outerjoin(AuditLog, AuditLog.record_id == cast(Permission.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(Permission.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(Permission.audit_logs),
                joinedload(Permission.audit_logs).joinedload(AuditLog.user),
                joinedload(Permission.audit_logs).joinedload(AuditLog.action),
            )
            .filter(trashed)  # Just trashed data
            .order_by(desc(Permission.id))  # Order by Permission.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        self.logger.log("info", f"Permission: {response}")

        # Count the total number of records without pagination
        count_query = (
            select(func.count(Permission.id)).select_from(Permission).filter(trashed)
        )
        if keywords:
            count_query = count_query.filter(Permission.name.ilike(f"{keywords}"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        print(total_count)

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

    async def find_trash(
        self, id: int, request: Request, session: AsyncSession
    ) -> Optional[Permission]:
        trashed = await AuditLog().is_trashed(Permission)
        q = (
            select(Permission)
            .options(
                joinedload(Permission.audit_logs),
                joinedload(Permission.audit_logs).joinedload(AuditLog.user),
                joinedload(Permission.audit_logs).joinedload(AuditLog.action),
            )
            .where(Permission.id == id)
            .filter(trashed)
        )
        permission = await session.execute(q)
        response = permission.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
            )
        return response

    async def restore(self, id: int, request: Request, session: AsyncSession) -> dict:
        response = await self.find_trash(id, request, session)
        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("RESTORE", session),
                "record_id": id,
                "model_name": Permission.__tablename__,
            },
            session=session,
        )

        return response
