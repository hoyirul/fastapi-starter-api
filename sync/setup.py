# sync/setup.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

"""
This module is used to manage database setup.
DON'T MODIFY THIS FILE UNLESS YOU KNOW WHAT YOU'RE DOING.
THIS FILE IS USED TO SETUP DATABASE.
"""

import asyncpg
import asyncio
from src.configs import Config


async def get_db_connection():
    """Function to get database connection"""
    connection = await asyncpg.connect(Config.DATABASE_URL.replace("+asyncpg", ""))
    return connection


async def execute_query(query: str, *params):
    """Execute a query (e.g., SELECT, INSERT, etc.)"""
    connection = await get_db_connection()
    try:
        result = await connection.fetch(query, *params)  # fetch for SELECT queries
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        await connection.close()


async def execute_update(query: str, *params):
    """Execute an update query (e.g., INSERT, UPDATE, DELETE)"""
    connection = await get_db_connection()
    try:
        result = await connection.execute(
            query, *params
        )  # execute for non-SELECT queries
        return result
    except Exception as e:
        print(f"Error executing update: {e}")
    finally:
        await connection.close()


# Function for testing the connection and running a query
async def main():
    connection = None
    try:
        connection = await get_db_connection()
        print("Database connected")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
    finally:
        if connection:
            await connection.close()
            print("Database connection closed")


if __name__ == "__main__":
    asyncio.run(main())
