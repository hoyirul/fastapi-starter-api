# src/modules/authentications/permissions/models.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional, List
import sqlalchemy as sa
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession

class Permission(SQLModel, table=True):
    __tablename__ = "mst_permissions"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True))
    description: Optional[str] = Field(sa_column=Column(pg.TEXT))
    role_permissions: Optional["RolePermission"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Permission.id == RolePermission.permission_id",
            "overlaps": "role_permissions",
        }
    )
    user_permissions: Optional["UserPermission"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Permission.id == UserPermission.permission_id",
            "overlaps": "user_permissions",
        }
    )
    audit_logs: Optional[List["AuditLog"]] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "(cast(Permission.id, String) == foreign(AuditLog.record_id)) & (AuditLog.model_name == 'mst_permissions')",
            "overlaps": "audit_logs",
        }
    )

    def __repr__(self):
        return f"<Permission {self.id}>"

    async def is_used(self, id: int, session: AsyncSession) -> bool:
        from src.modules.authentications.roles.models import RolePermission
        from src.modules.authentications.users.models import UserPermission

        query = select(RolePermission).filter(RolePermission.permission_id == id)
        result = await session.execute(query)
        role_permissions = result.scalars().all()

        query = select(UserPermission).filter(UserPermission.permission_id == id)
        result = await session.execute(query)
        user_permissions = result.scalars().all()

        return len(role_permissions) > 0 or len(user_permissions) > 0