# sync/seeders/ref_user_menus_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "ref_user_menus"


async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (user_id, menu_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6);
    """
    # await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
