# src/modules/logs/audit_logs/models.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import sqlalchemy as sa
from typing import List, Optional
from sqlmodel import select, cast, String


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    user_id: int = Field(sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_users.id")))
    action_id: int = Field(sa_column=Column(pg.BIGINT, sa.ForeignKey("mst_actions.id")))
    record_id: str = Field(sa_column=Column(pg.VARCHAR))
    ip_address: str = Field(sa_column=Column(pg.VARCHAR))
    model_name: str = Field(sa_column=Column(pg.VARCHAR))
    notes: str = Field(sa_column=Column(pg.VARCHAR))
    actioned_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "AuditLog.user_id == User.id",
            "overlaps": "user",
        }
    )
    action: Optional["Action"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "AuditLog.action_id == Action.id",
            "overlaps": "action",
        }
    )

    def __repr__(self):
        # you have to change this to your model fields to be displayed for example self.id
        return f"<AuditLog {self.id}>"

    async def is_created(self, model, primary_key=None):
        if primary_key:
            primaryKeyModel = getattr(model, primary_key)
        else:
            primaryKeyModel = model.id

        created = (
            select(AuditLog)
            .filter(
                AuditLog.record_id == cast(primaryKeyModel, String),
                AuditLog.action_id == 1,
                AuditLog.model_name == model.__tablename__,
            )
            .exists()
            .correlate(model)
        )

        return created

    async def is_updated(self, model, primary_key=None):
        if primary_key:
            primaryKeyModel = getattr(model, primary_key)
        else:
            primaryKeyModel = model.id

        updated = (
            select(AuditLog)
            .filter(
                AuditLog.record_id == cast(primaryKeyModel, String),
                AuditLog.action_id == 2,
                AuditLog.model_name == model.__tablename__,
            )
            .exists()
            .correlate(model)
        )

        return updated

    async def is_trashed(self, model, primary_key=None):
        if primary_key:
            primaryKeyModel = getattr(model, primary_key)
        else:
            primaryKeyModel = model.id

        trashed = (
            select(AuditLog)
            .filter(
                AuditLog.record_id == cast(primaryKeyModel, String),
                AuditLog.action_id == 3,
                AuditLog.model_name == model.__tablename__,
            )
            .exists()
            .correlate(model)
        )

        return trashed

    async def is_restored(self, model, primary_key=None):
        if primary_key:
            primaryKeyModel = getattr(model, primary_key)
        else:
            primaryKeyModel = model.id

        restored = (
            select(AuditLog)
            .filter(
                AuditLog.record_id == cast(primaryKeyModel, String),
                AuditLog.action_id == 4,
                AuditLog.model_name == model.__tablename__,
            )
            .exists()
            .correlate(model)
        )

        return restored
