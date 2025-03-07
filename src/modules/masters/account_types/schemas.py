# src/modules/masters/account_types/schemas.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from pydantic import validator
from src.modules.logs.audit_logs.schemas import AuditLogSchema
from src.utils.pagination import PaginationSchema


class AccountTypeSchema(BaseModel):
    id: int
    name: str
    audit_logs: Optional[
        List[AuditLogSchema]
    ]  # dont remove this line, it's for audit logs

    class Config:
        orm_mode = True


class AccountTypeResponseSchema(PaginationSchema):
    data: Optional[List[AccountTypeSchema]]

    # dont forget to add this config for the orm_mode
    class Config:
        orm_mode = True

class SelectAccountTypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class AccountTypeRequestSchema(BaseModel):
    name: str


# you can add more schemas if you need
