# src/modules/logs/audit_logs/schemas.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from src.utils.pagination import PaginationSchema

class UserAuditSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class ActionAuditSchema(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        orm_mode = True

class AuditLogSchema(BaseModel):
    user_id: int
    action_id: int
    record_id: str
    model_name: str
    notes: Optional[str]
    actioned_at: datetime
    user: Optional[UserAuditSchema]
    action: Optional[ActionAuditSchema]

    class Config:
        orm_mode = True

class AuditLogResponseSchema(PaginationSchema):
    data: Optional[List[AuditLogSchema]]

    class Config:
        orm_mode = True

class AuditLogRequestSchema(BaseModel):
    # Add your fields here
    pass


# you can add more schemas if you need
