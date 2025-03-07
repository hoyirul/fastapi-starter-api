# src/modules/authentications/roles/models.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional, List
import sqlalchemy as sa


class Role(SQLModel, table=True):
    __tablename__ = "mst_roles"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True))
    description: str = Field(sa_column=Column(pg.VARCHAR(255)))
    permissions: Optional[List["Permission"]] = Relationship(
        sa_relationship_kwargs={
            "secondary": "ref_role_permissions",
            "primaryjoin": "Role.id == ref_role_permissions.c.role_id",
            "secondaryjoin": "Permission.id == ref_role_permissions.c.permission_id",
            "overlaps": "permissions",
            "overlaps": "roles",
        }
    )
    audit_logs: Optional[List["AuditLog"]] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "(cast(Role.id, String) == foreign(AuditLog.record_id)) & (AuditLog.model_name == 'mst_roles')",
            "overlaps": "audit_logs",
        }
    )

    def __repr__(self):
        # you have to change this to your model fields to be displayed for example self.id
        return f"<Role {self.id}>"


class RolePermission(SQLModel, table=True):
    __tablename__ = "ref_role_permissions"
    __table_args__ = {"extend_existing": True}

    role_id: int = Field(
        sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_roles.id"), primary_key=True)
    )
    permission_id: int = Field(
        sa_column=Column(
            pg.BIGINT, sa.ForeignKey("mst_permissions.id"), primary_key=True
        )
    )
    role: Optional["Role"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "RolePermission.role_id == Role.id",
            "overlaps": "permissions,roles",
        }
    )
    permission: Optional["Permission"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "RolePermission.permission_id == Permission.id",
            "overlaps": "roles,permissions",
        }
    )

    def __repr__(self):
        # you have to change this to your model fields to be displayed for example self.id
        return f"<RolePermission role_id={self.role_id} permission_id={self.permission_id}>"
