# src/modules/authentications/permissions/models.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional, List
import sqlalchemy as sa


class Permission(SQLModel, table=True):
    __tablename__ = "mst_permissions"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True))
    description: Optional[str] = Field(sa_column=Column(pg.TEXT))
    # role_permissions: Optional["RolePermission"] = Relationship()
    # user_permissions: Optional["UserPermission"] = Relationship()
    audit_logs: Optional[List["AuditLog"]] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "(cast(Permission.id, String) == foreign(AuditLog.record_id)) & (AuditLog.model_name == 'mst_permissions')",
            "overlaps": "audit_logs",
        }
    )

    def __repr__(self):
        return f"<Permission {self.id}>"
