# src/modules/logs/actions/models.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import sqlalchemy as sa
from typing import List, Optional

# from src.modules.logs.audit_logs.models import AuditLog


class Action(SQLModel, table=True):
    __tablename__ = "mst_actions"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(100), unique=True))
    description: str = Field(sa_column=Column(pg.VARCHAR(255)))
    color: str = Field(sa_column=Column(pg.VARCHAR(25)))
    audit_logs: Optional[List["AuditLog"]] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "(cast(Action.id, String) == foreign(AuditLog.record_id)) & (AuditLog.model_name == 'mst_actions')",
            "overlaps": "audit_logs",
        }
    )

    def __repr__(self):
        # you have to change this to your model fields to be displayed for example self.id
        return f"<Action {self.id}>"
