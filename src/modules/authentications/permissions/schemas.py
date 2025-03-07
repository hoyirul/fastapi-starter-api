# src/modules/authentications/permissions/schemas.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from src.modules.logs.audit_logs.schemas import AuditLogSchema
from src.utils.pagination import PaginationSchema


class PermissionSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    audit_logs: Optional[List[AuditLogSchema]]

    class Config:
        orm_mode = True


class PermissionResponseSchema(PaginationSchema):
    data: Optional[List[PermissionSchema]]

    class Config:
        orm_mode = True

class SelectPermissionSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class PermissionRequestSchema(BaseModel):
    name: str
    description: Optional[str]
