# src/modules/logs/actions/schemas.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from pydantic import validator
from src.modules.logs.audit_logs.schemas import AuditLogSchema
from src.utils.pagination import PaginationSchema

class ColorSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ActionSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    color: str
    audit_logs: Optional[List[AuditLogSchema]]

    class Config:
        orm_mode = True

class ActionResponseSchema(PaginationSchema):
    data: Optional[List[ActionSchema]]

    class Config:
        orm_mode = True

class ActionRequestSchema(BaseModel):
    name: str
    description: Optional[str]
    color: str = 'gray'

    @validator("name")
    def validate_name(cls, v):
        if not v:
            raise ValueError("Name is required")
        return v

    @validator("description")
    def validate_description(cls, v):
        if not v:
            raise ValueError("Description is required")
        return v
    
    @validator("color")
    def validate_color(cls, v):
        if not v:
            raise ValueError("Color is required")
        return v
