# sync/seeders/mst_roles_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "mst_roles"


async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (name, description) VALUES
    ('Superadmin', 'Superadmin role'),
    ('Admin', 'Admin role'),
    ('Accountant', 'Accountant role'),
    ('Finance', 'Finance role'),
    ('Tax Officer', 'Tax Officer role'),
    ('User', 'User role');
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
