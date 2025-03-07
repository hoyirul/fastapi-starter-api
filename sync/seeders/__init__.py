# sync/seeders/__init__.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

"""
This module is used to manage database seeders.
DON'T MODIFY THIS FILE UNLESS YOU KNOW WHAT YOU'RE DOING.
THIS FILE IS USED TO RUN SEEDERS.
"""

import os
import importlib
from sync.setup import get_db_connection
from src.utils.logging import Logging

logger = Logging(level="DEBUG")


async def seed(table_name=None):
    connection = None
    try:
        connection = await get_db_connection()
        # Get all seeders and sort them in ascending order (001, 002, ...)
        seeder_files = [
            file
            for file in os.listdir(os.path.dirname(__file__))
            if file.endswith("_seeder.py") and file != "__init__.py"
        ]
        seeder_files.sort()  # Sort seeders in ascending order (001, 002, ...)

        for file in seeder_files:
            module = importlib.import_module(f".{file[:-3]}", "sync.seeders")

            # If table_name is provided, run seeding for that table only
            if table_name:
                if hasattr(module, "table") and module.table == table_name:
                    await module.seed(connection)
                    logger.log(
                        "info",
                        f"Seed data for table {table_name} has been applied.",
                    )
            else:
                # If no table_name is provided, run seeding for all seeders
                await module.seed(connection)
                logger.log("info", f"Seed data for {file} has been applied.")
    except Exception as e:
        logger.log("error", f"Seed data failed: {e}")
    finally:
        if connection:
            await connection.close()
            logger.log("info", "Database connection closed after seeding.")


async def rollback(table_name=None):
    connection = None
    try:
        connection = await get_db_connection()
        # Get all seeders and sort them in descending order (002, 001, ...)
        seeder_files = [
            file
            for file in os.listdir(os.path.dirname(__file__))
            if file.endswith("_seeder.py") and file != "__init__.py"
        ]
        seeder_files.sort(
            reverse=True
        )  # Sort seeders in descending order (002, 001, ...)

        for file in seeder_files:
            module = importlib.import_module(f".{file[:-3]}", "sync.seeders")

            # If table_name is provided, run rollback for that table only
            if table_name:
                if hasattr(module, "table") and module.table == table_name:
                    await module.rollback(connection)
                    logger.log(
                        "info",
                        f"Clear seed data for table {table_name} has been applied.",
                    )
            else:
                # If no table_name is provided, run rollback for all seeders
                await module.rollback(connection)
                logger.log("info", f"Clear seed data for {file} has been applied.")
    except Exception as e:
        logger.log("error", f"Clear seed data failed: {e}")
    finally:
        if connection:
            await connection.close()
            logger.log("info", "Database connection closed after rollback.")
