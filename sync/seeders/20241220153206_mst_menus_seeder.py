# sync/seeders/mst_menus_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "mst_menus"


async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (parent_id, name, description) VALUES
    (NULL, 'Home', 'Main homepage'),
    (NULL, 'About Us', 'Information about the company'),
    (NULL, 'Contact', 'Contact us page');
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
