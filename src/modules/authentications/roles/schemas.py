# src/modules/authentications/roles/schemas.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from src.modules.logs.audit_logs.schemas import AuditLogSchema
from src.utils.pagination import PaginationSchema


class PermissionSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class RoleSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    permissions: Optional[List[PermissionSchema]]
    audit_logs: Optional[List[AuditLogSchema]]

    class Config:
        orm_mode = True


class RoleResponseSchema(PaginationSchema):
    data: Optional[List[RoleSchema]]

    class Config:
        orm_mode = True

class SelectRoleSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class RoleRequestSchema(BaseModel):
    name: str
    description: Optional[str]


class GivePermissionToRoleSchema(BaseModel):
    role_id: int
    permission_id: List[int]
