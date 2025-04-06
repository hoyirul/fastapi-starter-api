# src/utils/actions.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi.exceptions import HTTPException
from fastapi import status
from .logging import Logging


class ActionType:
    def __init__(self):
        self.logger = Logging(level="DEBUG")

    async def __call__(self, action_type: str, session: AsyncSession) -> int:
        from src.modules.logs.actions.models import Action

        # V1
        # action_type = action_type.capitalize()
        # V2
        action_type = action_type.upper()

        # Convert action type to singular
        q = select(Action).where(Action.name == action_type)
        action = await session.execute(q)
        response = action.scalars().first()

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Action not found"
            )

        # return response.id
        return response.id
