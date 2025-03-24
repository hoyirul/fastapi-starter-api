# sync/seeders/mst_users_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from src.utils.security import password_hash

table = "mst_users"

password = password_hash("password")


async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO mst_users (name, email, password)
    VALUES 
    ('Super Admin', 'superadmin@mail.com', '{password}'),
    ('Admin', 'admin@mail.com', '{password}'),
    ('User', 'user@mail.com', '{password}');
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
