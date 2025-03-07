# sync/migrations/__init__.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

"""
This module is used to manage database migrations.
DON'T MODIFY THIS FILE UNLESS YOU KNOW WHAT YOU'RE DOING.
THIS FILE IS USED TO RUN MIGRATIONS.
"""

import os
import importlib
from sync.setup import get_db_connection
from src.utils.logging import Logging

logger = Logging(level="DEBUG")


async def upgrade(table_name=None, alter=False):
    connection = None
    try:
        connection = await get_db_connection()
        for file in os.listdir(os.path.dirname(__file__)):
            if file.endswith(".py") and file != "__init__.py":
                # Migration module import
                module = importlib.import_module(f".{file[:-3]}", "sync.migrations")

                # If table_name is given, run upgrade for that table
                if table_name and alter is False:
                    if hasattr(module, "table") and module.table == table_name:
                        await module.upgrade(connection)
                        logger.log(
                            "info",
                            f"Migration for table {table_name} has been applied.",
                        )
                elif alter is True:
                    if (
                        hasattr(module, "alter_table")
                        and module.alter_table == table_name
                    ):
                        await module.upgrade(connection)
                        logger.log(
                            "info",
                            f"Migration for table {table_name} has been applied.",
                        )
                else:
                    # if table_name is not given, run all migrations
                    if hasattr(module, "alter_table"):
                        continue
                    else:
                        await module.upgrade(connection)
                        logger.log("info", f"Upgrade for {file} has been applied.")

    except Exception as e:
        logger.log("error", f"Migration upgrade failed: {e}")
    finally:
        if connection:
            await connection.close()
            logger.log("info", "Database connection closed after upgrade.")


async def downgrade(table_name=None, alter=False):
    connection = None
    try:
        connection = await get_db_connection()
        # Get migration files and sort them in descending order (002, 001, ...)
        migration_files = [
            file
            for file in os.listdir(os.path.dirname(__file__))
            if file.endswith(".py") and file != "__init__.py"
        ]
        migration_files.sort(reverse=True)  # Sort the files in descending order

        for file in migration_files:
            module = importlib.import_module(f".{file[:-3]}", "sync.migrations")

            # If table_name is provided, run migration for that table
            if table_name and alter is False:
                if hasattr(module, "table") and module.table == table_name:
                    await module.downgrade(connection)
                    logger.log(
                        "info",
                        f"Downgrade for table {table_name} has been applied.",
                    )
            elif alter is True:
                if hasattr(module, "alter_table") and module.alter_table == table_name:
                    await module.downgrade(connection)
                    logger.log(
                        "info",
                        f"Downgrade for table {table_name} has been applied.",
                    )
            else:
                # Run all migrations
                if hasattr(module, "alter_table"):
                    continue
                else:
                    await module.downgrade(connection)
                logger.log("info", f"Downgrade for {file} has been applied.")

    except Exception as e:
        logger.log("error", f"Migration downgrade failed: {e}")
    finally:
        if connection:
            await connection.close()
            logger.log("info", "Database connection closed after downgrade.")
