# src/modules/authentications/auth/schemas.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class AuthSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role_id: int
    role: str
    active: bool = True
    last_logged_in: Optional[datetime] = None

    class Config:
        orm_mode = True

class LoginRequestSchema(BaseModel):
    email: str = Field(max_length=100)
    password: str = Field(min_length=6)

class SwitchAccountRequestSchema(BaseModel):
    email: str = Field(max_length=100)

class ChangePasswordRequestSchema(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)

class RegisterRequestSchema(BaseModel):
    name: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password: str = Field(min_length=6)
