# src/utils/pagination.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from pydantic import BaseModel
from typing import List, Optional


# Schema for pagination
class PaginationSchema(BaseModel):
    current_page: int
    total_count: int
    per_page: int
    total_pages: int

    class Config:
        orm_mode = True
