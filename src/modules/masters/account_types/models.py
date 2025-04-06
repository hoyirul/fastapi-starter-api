# src/modules/masters/account_types/models.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import sqlalchemy as sa
from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession

class AccountType(SQLModel, table=True):
    __tablename__ = "mst_account_types"
    __table_args__ = {"extend_existing": True}

    id: int = Field(sa_column=Column(pg.BIGINT, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True))
    audit_logs: Optional[List["AuditLog"]] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "(cast(AccountType.id, String) == foreign(AuditLog.record_id)) & (AuditLog.model_name == 'mst_account_types')",
            "overlaps": "audit_logs",
        }
    )

    def __repr__(self):
        # you have to change this to your model fields to be displayed for example self.id
        return f"<AccountType {self.id}>"

    async def is_used(self, id: int, session: AsyncSession) -> bool:
        from src.modules.masters.accounts.models import Account

        query = select(Account).filter(Account.account_type_id == id)
        result = await session.execute(query)
        accounts = result.scalars().all()
        return len(accounts) > 0