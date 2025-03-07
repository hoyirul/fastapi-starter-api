# src/modules/authentications/menus/models.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import sqlalchemy as sa
from typing import List, Optional


class Menu(SQLModel, table=True):
    __tablename__ = "mst_menus"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    # default null
    parent_id: Optional[int] = Field(sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_menus.id"), nullable=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True))
    alias: str = Field(sa_column=Column(pg.VARCHAR(255)))
    link: Optional[str] = Field(sa_column=Column(pg.VARCHAR(255)))
    icon: Optional[str] = Field(sa_column=Column(pg.VARCHAR(255)))
    ordering: int = Field(sa_column=Column(pg.INTEGER))
    parent: Optional["Menu"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Menu.parent_id == Menu.id",
            "uselist": False,
        }
    )
    audit_logs: Optional[List["AuditLog"]] = Relationship(
        sa_relationship_kwargs={"primaryjoin":"(cast(Menu.id, String) == foreign(AuditLog.record_id)) & (AuditLog.model_name == 'mst_menus')"}
    )

    def __repr__(self):
        # you have to change this to your model fields to be displayed for example self.id
        return f"<Menu {self.id}>"

class RoleMenu(SQLModel, table=True):
    __tablename__ = "ref_role_menus"
    __table_args__ = {"extend_existing": True}

    role_id: int = Field(
        sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_roles.id"), primary_key=True)
    )
    menu_id: int = Field(
        sa_column=Column(
            pg.BIGINT, sa.ForeignKey("mst_menus.id"), primary_key=True
        )
    )
    role: Optional["Role"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "RoleMenu.role_id == Role.id",
            "overlaps": "permissions,roles",
        }
    )
    menu: Optional["Menu"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "RoleMenu.menu_id == Menu.id",
        }
    )

class UserMenu(SQLModel, table=True):
    __tablename__ = "ref_user_menus"
    __table_args__ = {"extend_existing": True}

    user_id: int = Field(
        sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_users.id"), primary_key=True)
    )
    menu_id: int = Field(
        sa_column=Column(
            pg.BIGINT, sa.ForeignKey("mst_menus.id"), primary_key=True
        )
    )
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "UserMenu.user_id == User.id",
            "overlaps": "permissions,roles",
        }
    )
    menu: Optional["Menu"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "UserMenu.menu_id == Menu.id",
        }
    )