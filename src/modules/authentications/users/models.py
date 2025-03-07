# src/modules/authentications/users/models.py
# -*- coding: utf-8 -*-

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional, List
import sqlalchemy as sa


class User(SQLModel, table=True):
    __tablename__ = "mst_users"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(255)))
    email: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True))
    password: str = Field(sa_column=Column(pg.VARCHAR(255)))
    active: bool = Field(sa_column=Column(pg.BOOLEAN, default=True))
    role: Optional["Role"] = Relationship(
        sa_relationship_kwargs={
            "secondary": "ref_user_roles",
            "primaryjoin": "User.id == ref_user_roles.c.user_id",
            "secondaryjoin": "Role.id == ref_user_roles.c.role_id",
            "overlaps": "role",
        }
    )
    permissions: Optional[List["Permission"]] = Relationship(
        sa_relationship_kwargs={
            "secondary": "ref_user_permissions",
            "primaryjoin": "User.id == ref_user_permissions.c.user_id",
            "secondaryjoin": "Permission.id == ref_user_permissions.c.permission_id",
            "overlaps": "permissions",
        }
    )
    audit_logs: Optional[List["AuditLog"]] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "(cast(User.id, String) == foreign(AuditLog.record_id)) & (AuditLog.model_name == 'mst_users')",
            "overlaps": "audit_logs",
        }
    )

    def __repr__(self):
        return f"<User {self.id}>"


class UserPermission(SQLModel, table=True):
    __tablename__ = "ref_user_permissions"
    __table_args__ = {"extend_existing": True}

    user_id: int = Field(
        sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_users.id"), primary_key=True)
    )
    permission_id: int = Field(
        sa_column=Column(
            pg.BIGINT, sa.ForeignKey("mst_permissions.id"), primary_key=True
        )
    )
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "UserPermission.user_id == User.id",
            "overlaps": "users, permissions",
        }
    )
    permission: Optional["Permission"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "UserPermission.permission_id == Permission.id",
            "overlaps": "permissions, users",
        }
    )

    def __repr__(self):
        return f"<UserPermission user_id={self.user_id} permission_id={self.permission_id}>"


class UserRole(SQLModel, table=True):
    __tablename__ = "ref_user_roles"
    __table_args__ = {"extend_existing": True}

    user_id: int = Field(
        sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_users.id"), primary_key=True)
    )
    role_id: int = Field(
        sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_roles.id"), primary_key=True)
    )
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "UserRole.user_id == User.id",
            "overlaps": "user, role",
        }
    )
    role: Optional["Role"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "UserRole.role_id == Role.id",
            "overlaps": "role, user",
        }
    )

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"
