# sync/migrations/__init__.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

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

        # Ambil semua file Python (.py) dalam folder ini, kecuali __init__.py
        files = [file for file in os.listdir(os.path.dirname(__file__)) if file.endswith(".py") and file != "__init__.py"]

        # Urutkan file berdasarkan timestamp di awal nama file (asumsi formatnya seperti 20241221082857)
        files.sort(key=lambda file: int(file.split('_')[0]))  # Mengambil angka di awal nama file dan mengurutkannya

        # Iterasi setiap file yang sudah diurutkan
        for file in files:
            # Import module migration
            module = importlib.import_module(f".{file[:-3]}", "sync.migrations")
            
            # Jika table_name diberikan, jalankan upgrade untuk table tersebut
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
                # Jika table_name tidak diberikan, jalankan semua migration
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
        
        # Ambil semua file Python (.py) dalam folder ini, kecuali __init__.py
        migration_files = [
            file
            for file in os.listdir(os.path.dirname(__file__))
            if file.endswith(".py") and file != "__init__.py"
        ]

        # Urutkan file berdasarkan timestamp yang ada di awal nama file dalam urutan menurun (descending)
        migration_files.sort(key=lambda file: int(file.split('_')[0]), reverse=True)  # Mengurutkan dengan reverse=True

        # Iterasi setiap file yang sudah diurutkan
        for file in migration_files:
            # Import module migration
            module = importlib.import_module(f".{file[:-3]}", "sync.migrations")

            # Jika table_name diberikan, jalankan downgrade untuk table tersebut
            if table_name and alter is False:
                if hasattr(module, "table") and module.table == table_name:
                    await module.downgrade(connection)
                    logger.log(
                        "info",
                        f"Downgrade for table {table_name} has been applied.",
                    )
            elif alter is True:
                if (
                    hasattr(module, "alter_table")
                    and module.alter_table == table_name
                ):
                    await module.downgrade(connection)
                    logger.log(
                        "info",
                        f"Downgrade for table {table_name} has been applied.",
                    )
            else:
                # Jika table_name tidak diberikan, jalankan semua downgrade
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
