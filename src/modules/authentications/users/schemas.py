# src/modules/authentications/users/schemas.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from src.modules.logs.audit_logs.schemas import AuditLogSchema
from src.utils.pagination import PaginationSchema


class RoleSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class PermissionSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str
    active: bool
    role: Optional[RoleSchema]
    permissions: Optional[List[PermissionSchema]]
    audit_logs: Optional[List[AuditLogSchema]]

    class Config:
        orm_mode = True


class UserResponseSchema(PaginationSchema):
    data: Optional[List[UserSchema]]

    class Config:
        orm_mode = True

class SelectUserSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class UserRequestSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool] = True

class UserUpdateRequestSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    active: Optional[bool]


class AssignRoleSchema(BaseModel):
    user_id: int
    role_id: int

class RevokeRoleSchema(BaseModel):
    user_id: int
    role_id: int

class GivePermissionToUserSchema(BaseModel):
    user_id: int
    permission_id: List[int]
