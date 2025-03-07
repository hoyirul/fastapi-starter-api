# sync/seeders/ref_user_permissions_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "ref_user_permissions"


async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (user_id, permission_id) VALUES
    (1, 1),
    (1, 10);
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
