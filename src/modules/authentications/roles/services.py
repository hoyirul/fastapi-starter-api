# src/modules/authentications/roles/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .schemas import (
    RoleRequestSchema, 
    GivePermissionToRoleSchema, 
    RoleSchema,
    SelectRoleSchema
)
from .models import Role
from src.modules.logs.audit_logs.models import AuditLog
from sqlmodel import select, desc, cast, String
from fastapi import status, Request
from typing import Optional
from sqlalchemy.orm import joinedload
from src.utils.logging import Logging, ActivityLog
from src.utils.actions import ActionType
from sqlalchemy import func


class RoleService:
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
        trashed = await AuditLog().is_trashed(Role)

        # Build the query for fetching roles
        q = (
            select(Role)
            .distinct()  # This will ensure only unique Role records are returned
            .select_from(Role)
            .outerjoin(AuditLog, AuditLog.record_id == cast(Role.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(Role.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(Role.permissions),
                joinedload(Role.audit_logs),
                joinedload(Role.audit_logs).joinedload(AuditLog.user),
                joinedload(Role.audit_logs).joinedload(AuditLog.action),
            )
            .filter(~trashed)  # Exclude trashed roles
            .order_by(desc(Role.id))  # Order by Role.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for roles data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = select(func.count(Role.id)).select_from(Role).filter(~trashed)
        if keywords:
            count_query = count_query.filter(Role.name.ilike(f"%{keywords}%"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (
            total_count + limit - 1
        ) // limit  # This is the ceiling of total_count / limit

        # Calculate the current page based on skip and limit
        current_page = skip // limit + 1 if total_count > 0 else 0

        # Return the roles along with pagination information
        return {
            "current_page": current_page,
            "total_count": total_count,
            "per_page": limit,
            "total_pages": total_pages,
            "data": response,
        }

    async def find(
        self, id: int, request: Request, session: AsyncSession
    ) -> Optional[RoleSchema]:
        trashed = await AuditLog().is_trashed(Role)
        q = (
            select(Role)
            .options(
                joinedload(Role.permissions),
                joinedload(Role.audit_logs),
                joinedload(Role.audit_logs).joinedload(AuditLog.user),
                joinedload(Role.audit_logs).joinedload(AuditLog.action),
            )
            .where(Role.id == id)
            .filter(~trashed)
        )
        role = await session.execute(q)
        response = role.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            )
        return response

    async def select(self, request: Request, session: AsyncSession) -> list:
        trashed = await AuditLog().is_trashed(Role)
        q = select(Role).filter(~trashed)
        result = await session.execute(q)
        response = result.scalars().all()

        return response

    async def create(
        self, request: Request, body: RoleRequestSchema, session: AsyncSession
    ) -> dict:
        body = Role(**body.dict())
        session.add(body)
        await session.commit()

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("CREATE", session),
                "record_id": body.id,
                "model_name": Role.__tablename__,
            },
            session=session,
        )
        return body

    async def update(
        self, id: int, request: Request, body: RoleRequestSchema, session: AsyncSession
    ) -> dict:
        response = await self.find(id, request, session)
        for key, value in body.dict().items():
            setattr(response, key, value)
        await session.commit()

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("UPDATE", session),
                "record_id": id,
                "model_name": Role.__tablename__,
            },
            session=session,
        )

        return response

    async def give_permission_to_role(
        self, request: Request, body: GivePermissionToRoleSchema, session: AsyncSession
    ) -> dict:
        from src.modules.authentications.permissions.services import PermissionService
        try:
            role = await self.find(body.role_id, request, session)
            # body.permission_id is list of permission_id
            permissions = []
            for permission_id in body.permission_id:
                permission = await PermissionService().find(permission_id, request, session)
                permissions.append(permission.name)
                role.permissions.append(permission)
            await session.commit()

            return {
                "status": "success",
                "message": f"Permission {permissions} has been assigned to role {body.role_id}",
            }
        except Exception as e:
            await session.rollback()
            return {"status": "error", "message": str(e)}
    
    async def revoke_permission_to_role(
        self, request: Request, body: GivePermissionToRoleSchema, session: AsyncSession
    ) -> dict:
        from src.modules.authentications.permissions.services import PermissionService
        try:

            role = await self.find(body.role_id, request, session)
            # body.permission_id is list of permission_id
            permissions = []
            for permission_id in body.permission_id:
                permission = await PermissionService().find(permission_id, request, session)
                permissions.append(permission.name)
                role.permissions.remove(permission)
            await session.commit()

            return {
                "status": "success",
                "message": f"Permission {permissions} has been revoked from role {body.role_id}",
            }
        except Exception as e:
            await session.rollback()
            return {"status": "error", "message": str(e)}

    async def destroy(self, id: int, request: Request, session: AsyncSession) -> dict:
        response = await self.find(id, request, session)

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("DELETE", session),
                "record_id": id,
                "model_name": Role.__tablename__,
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
        trashed = await AuditLog().is_trashed(Role)

        # Build the query for fetching roles
        q = (
            select(Role)
            .distinct()  # This will ensure only unique Role records are returned
            .select_from(Role)
            .outerjoin(AuditLog, AuditLog.record_id == cast(Role.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(Role.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(Role.permissions),
                joinedload(Role.audit_logs),
                joinedload(Role.audit_logs).joinedload(AuditLog.user),
                joinedload(Role.audit_logs).joinedload(AuditLog.action),
            )
            .filter(trashed)  # Just trashed roles
            .order_by(desc(Role.id))  # Order by Role.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for roles data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = select(func.count(Role.id)).select_from(Role).filter(trashed)
        if keywords:
            count_query = count_query.filter(Role.name.ilike(f"%{keywords}%"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (
            total_count + limit - 1
        ) // limit  # This is the ceiling of total_count / limit

        # Calculate the current page based on skip and limit
        current_page = skip // limit + 1 if total_count > 0 else 0

        # Return the roles along with pagination information
        return {
            "current_page": current_page,
            "total_count": total_count,
            "per_page": limit,
            "total_pages": total_pages,
            "data": response,
        }

    async def find_trash(
        self, id: int, request: Request, session: AsyncSession
    ) -> Optional[RoleSchema]:
        trashed = await AuditLog().is_trashed(Role)
        q = (
            select(Role)
            .options(
                joinedload(Role.permissions),
                joinedload(Role.audit_logs),
                joinedload(Role.audit_logs).joinedload(AuditLog.user),
                joinedload(Role.audit_logs).joinedload(AuditLog.action),
            )
            .where(Role.id == id)
            .filter(trashed)
        )
        role = await session.execute(q)
        response = role.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            )
        return response

    async def restore(self, id: int, request: Request, session: AsyncSession) -> dict:
        response = await self.find(id, request, session)

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("RESTORE", session),
                "record_id": id,
                "model_name": Role.__tablename__,
            },
            session=session,
        )

        return response
