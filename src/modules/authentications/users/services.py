# src/modules/authentications/users/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .schemas import UserRequestSchema
from .models import User, UserRole
from .schemas import (
    UserSchema, 
    AssignRoleSchema, 
    RevokeRoleSchema,
    GivePermissionToUserSchema,
    SelectUserSchema
)
from src.modules.authentications.roles.models import Role
from src.modules.logs.audit_logs.models import AuditLog
from sqlmodel import select, desc, cast, String
from fastapi import status, Request
from typing import Optional
from sqlalchemy.orm import joinedload
from src.utils.logging import Logging, ActivityLog
from src.utils.actions import ActionType
from sqlalchemy import func
from src.utils.security import password_hash


class UserService:
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
        trashed = await AuditLog().is_trashed(User)

        # Build the query for fetching users
        q = (
            select(User)
            .distinct()  # This will ensure only unique User records are returned
            .select_from(User)
            .outerjoin(AuditLog, AuditLog.record_id == cast(User.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(User.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(User.role),
                joinedload(User.permissions),
                joinedload(User.audit_logs),
                joinedload(User.audit_logs).joinedload(AuditLog.user),
                joinedload(User.audit_logs).joinedload(AuditLog.action),
            )
            .filter(~trashed)  # Exclude trashed users
            .order_by(desc(User.id))  # Order by User.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for users data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = select(func.count(User.id)).select_from(User).filter(~trashed)
        if keywords:
            count_query = count_query.filter(User.name.ilike(f"%{keywords}%"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (
            total_count + limit - 1
        ) // limit  # This is the ceiling of total_count / limit

        # Calculate the current page based on skip and limit
        current_page = skip // limit + 1 if total_count > 0 else 0

        # Return the users along with pagination information
        return {
            "current_page": current_page,
            "total_count": total_count,
            "per_page": limit,
            "total_pages": total_pages,
            "data": response,
        }

    async def find(
        self, id: int, request: Request, session: AsyncSession
    ) -> Optional[UserSchema]:
        q = (
            select(User)
            .options(
                joinedload(User.role),
                joinedload(User.permissions),
                joinedload(User.audit_logs),
                joinedload(User.audit_logs).joinedload(AuditLog.user),
                joinedload(User.audit_logs).joinedload(AuditLog.action),
            )
            .where(User.id == id)
        )
        user = await session.execute(q)
        response = user.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return response

    async def select(self, request: Request, session: AsyncSession) -> list:
        trashed = await AuditLog().is_trashed(User)
        q = select(User).filter(~trashed)
        result = await session.execute(q)
        response = result.scalars().all()
        
        return response

    async def find_by_email(
        self, email: str, request: Request, session: AsyncSession
    ) -> bool:
        q = (
            select(User)
            .options(
                joinedload(User.role),
                joinedload(User.permissions),
                joinedload(User.audit_logs),
                joinedload(User.audit_logs).joinedload(AuditLog.user),
                joinedload(User.audit_logs).joinedload(AuditLog.action),
            )
            .where(User.email == email)
        )
        user = await session.execute(q)
        response = user.scalars().first()
        if response is None:
            return False
        
        return True

    async def create(
        self, request: Request, body: UserRequestSchema, session: AsyncSession
    ) -> dict:
        # If email is already exist
        if await self.find_by_email(body.email, request, session):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {body.email} already exist, please use another email",
            )

        body.password = password_hash(body.password)
        body = User(**body.dict())
        session.add(body)
        await session.commit()

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("CREATE", session),
                "record_id": body.id,
                "model_name": User.__tablename__,
            },
            session=session,
        )

        return body

    async def update(
        self, id: int, request: Request, body: UserRequestSchema, session: AsyncSession
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
                "model_name": User.__tablename__,
            },
            session=session,
        )

        return response

    async def assign_role(
        self, request: Request, body: AssignRoleSchema, session: AsyncSession
    ) -> dict:
        from src.modules.authentications.roles.services import RoleService
        try:

            user = await self.find(body.user_id, request, session)
            role = await RoleService().find(body.role_id, request, session)
            user.role = role
            await session.commit()

            return {
                "status": "success",
                "message": f"Role {role.name} has been assigned to user {user.name}",
            }
        except Exception as e:
            await session.rollback()
            return {"status": "error", "message": str(e)}

    async def revoke_role(
        self, request: Request, body: RevokeRoleSchema, session: AsyncSession
    ) -> dict:
        from src.modules.authentications.roles.services import RoleService
        try:
            user = await self.find(body.user_id, request, session)
            role = await RoleService().find(body.role_id, request, session)
            # remove 
            user.role = None
            await session.commit()

            return {
                "status": "success",
                "message": f"Role {role.name} has been revoked from user {user.name}",
            }
        except Exception as e:
            await session.rollback()
            return {"status": "error", "message": str(e)}

    async def give_permission_to_user(
        self,
        request: Request,
        body: GivePermissionToUserSchema,
        session: AsyncSession,
    ) -> dict:
        from src.modules.authentications.permissions.services import PermissionService
        
        try:
            user = await self.find(body.user_id, request, session)
            # body.permission_id is list of permission_id
            permissions = []
            for permission_id in body.permission_id:
                permission = await PermissionService().find(permission_id, request, session)
                permissions.append(permission.name)
                user.permissions.append(permission)
            await session.commit()

            user.permissions.append(permission)
            await session.commit()

            return {
                "status": "success",
                "message": f"Permission {permissions} has been assigned to user {user.name}",
            }
        except Exception as e:
            await session.rollback()
            return {"status": "error", "message": str(e)}

    async def revoke_permission_to_user(
        self,
        request: Request,
        body: GivePermissionToUserSchema,
        session: AsyncSession,
    ) -> dict:
        from src.modules.authentications.permissions.services import PermissionService
        try:
            user = await self.find(body.user_id, request, session)
            # body.permission_id is list of permission_id
            permissions = []
            for permission_id in body.permission_id:
                permission = await PermissionService().find(permission_id, request, session)
                permissions.append(permission.name)
                user.permissions.remove(permission)
            await session.commit()

            return {
                "status": "success",
                "message": f"Permission {permissions} has been revoked from user {user.name}",
            }
        except Exception as e:
            await session.rollback()
            return {"status": "error", "message": str(e)}

    async def inactive(self, id: int, request: Request, session: AsyncSession) -> dict:
        response = await self.find(id, request, session)
        response.active = False
        await session.commit()

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("UPDATE", session),
                "record_id": response.id,
                "model_name": User.__tablename__,
            },
            session=session,
        )

        return response

    async def active(self, id: int, request: Request, session: AsyncSession) -> dict:
        response = await self.find(id, request, session)
        response.active = True
        response.failed_login_attempts = 0
        await session.commit()

        await self.activity_log(
            request=request,
            body={
                "action_id": await self.action_type("UPDATE", session),
                "record_id": response.id,
                "model_name": User.__tablename__,
            },
            session=session,
        )

        return response
