
# sync/seeders/ref_user_companies_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "ref_user_companies"

async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (user_id, company_id, status) VALUES
    (1, 'C00001', 'approved'),
    (2, 'C00001', 'approved'),
    (3, 'C00001', 'approved'),
    (4, 'C00001', 'approved'),
    (5, 'C00001', 'approved'),
    (6, 'C00001', 'approved');
    """
    await engine.execute(query)

async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
