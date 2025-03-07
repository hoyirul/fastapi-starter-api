# src/startup.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

import logging
from src.databases import db  # Ensure db contains engine and session configurations
from src.databases.redis import (
    RedisDB,
)  # Ensure redisDB contains RedisDB configurations
from src.utils.logging import Logging  # Import Logger class
from datetime import datetime

# Create an instance of the Logger class
logger = Logging(level="INFO")
redisDB = RedisDB()


async def on_startup():
    """
    This function is called when the application starts.
    """
    try:
        # Attempt to connect to the database
        async with db.engine.connect() as conn:
            logger.log(
                "info", "Database connected successfully."
            )  # Log success message

        # Attempt to connect to the Redis database
        if redisDB.is_connected:
            logger.log("info", "Redis connected successfully.")
        else:
            logger.log("error", "Failed to connect to Redis.")

    except Exception as e:
        # Log the error if connection fails
        logger.log("error", f"Failed to connect to the database: {str(e)}")
        raise  # Raise the exception to stop the application from starting


async def on_shutdown():
    """
    This function is called when the application stops.
    """
    try:
        # Attempt to verify or disconnect the database
        async with db.engine.connect() as conn:
            logger.log(
                "info", "Database disconnected successfully."
            )  # Log success message
    except Exception as e:
        # Log the error if disconnect fails
        logger.log("error", f"Failed to disconnect from the database: {str(e)}")
