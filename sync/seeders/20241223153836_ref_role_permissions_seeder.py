# sync/seeders/ref_role_permissions_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "ref_role_permissions"


async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (role_id, permission_id) VALUES
    (1, 1),
    (1, 3),
    (1, 6),
    (1, 18),
    (1, 29),
    (1, 38),
    (1, 51),
    (1, 60),
    (1, 69),
    (1, 78),
    (1, 87),
    (1, 96),
    (1, 105),
    (1, 115),
    (1, 124),
    (1, 133),
    (1, 142),
    (1, 151),
    (1, 160);
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
