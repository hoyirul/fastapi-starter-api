
# sync/seeders/mst_companies_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "mst_companies"

async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (id, name, address, contact_email) VALUES
    ('C00001', 'Apple Silicon', 'Jl. Raya Kebayoran Lama No. 12', 'support@apple.com');
    """
    await engine.execute(query)

async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
