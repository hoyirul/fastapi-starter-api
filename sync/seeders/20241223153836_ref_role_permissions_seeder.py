# sync/seeders/ref_role_permissions_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

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
    (1, 52),
    (1, 61),
    (1, 70),
    (1, 79),
    (1, 88),
    (1, 97),
    (1, 106),
    (1, 116),
    (1, 125),
    (1, 134),
    (1, 143),
    (1, 152),
    (1, 161);
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
