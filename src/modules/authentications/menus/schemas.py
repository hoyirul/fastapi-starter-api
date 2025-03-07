# src/modules/authentications/menus/schemas.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from pydantic import validator
from src.modules.logs.audit_logs.schemas import AuditLogSchema
from src.utils.pagination import PaginationSchema

class MenuHierarchySchema(BaseModel):
    id: int
    parent_id: Optional[int]
    name: str
    alias: str
    link: Optional[str]
    icon: Optional[str]
    ordering: int
    children: Optional[List["MenuHierarchySchema"]] = []

    class Config:
        orm_mode = True

class MenuSchema(BaseModel):
    id: int
    parent_id: Optional[int]
    name: str
    alias: str
    link: Optional[str]
    icon: Optional[str]
    ordering: int
    audit_logs: Optional[List[AuditLogSchema]] # dont remove this line, it's for audit logs

    class Config:
        orm_mode = True

class MenuResponseSchema(PaginationSchema):
    data: Optional[List[MenuSchema]]

    # dont forget to add this config for the orm_mode
    class Config:
        orm_mode = True

class SelectMenuSchema(BaseModel):
    id: int
    parent_id: Optional[int]
    name: str

    class Config:
        orm_mode = True

class MenuRequestSchema(BaseModel):
    parent_id: Optional[int]
    name: str
    alias: str
    link: Optional[str]
    icon: Optional[str]
    ordering: int

    class Config:
        orm_mode = True

class GiveMenuToRoleSchema(BaseModel):
    role_id: int
    menu_id: List[int]

    class Config:
        orm_mode = True

class GiveMenuToUserSchema(BaseModel):
    user_id: int
    menu_id: List[int]

    class Config:
        orm_mode = True

# you can add more schemas if you need
