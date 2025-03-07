# src/databases/db.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

import logging
from fastapi.exceptions import HTTPException
from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.configs import Config
from src.utils.logging import Logging

# Configure logging for SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)

# Create engine
engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=False,  # Turn off SQL echo log
    )
)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Database:
    def __init__(self):
        self.engine = engine
        self.session_maker = Session

    # for checking the connection
    async def connection(self) -> None:
        try:
            async with self.engine.connect() as conn:
                raise HTTPException(status_code=200, detail="Database connected")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to connect to database: {e}"
            )

    # for getting the session
    async def session(self) -> AsyncSession:
        # try:
        async with self.session_maker() as session:
            try:
                yield session
            finally:
                await session.close()
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"Failed to get session: {e}")
