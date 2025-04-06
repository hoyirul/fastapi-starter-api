# src/modules/authentications/auth/models.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional, List
import sqlalchemy as sa

class Auth(SQLModel, table=True):
    __tablename__ = "mst_users"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(255)))
    email: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True))
    password: str = Field(sa_column=Column(pg.VARCHAR(255)))
    active: bool = Field(sa_column=Column(pg.BOOLEAN, default=True))
    last_logged_in: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=None))
    failed_login_attempts: int = Field(sa_column=Column(pg.INTEGER, default=0))
    role: Optional["Role"] = Relationship(
        sa_relationship_kwargs={
            "secondary": "ref_user_roles",
            "primaryjoin": "User.id == ref_user_roles.c.user_id",
            "secondaryjoin": "Role.id == ref_user_roles.c.role_id",
            "overlaps": "role",
        }
    )

    def __repr__(self):
        return f"<User {self.id}>"