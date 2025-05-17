
# sync/seeders/trs_subscriptions_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "trs_subscriptions"

async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (user_id, subscription_plan_id, start_date, end_date, is_active, auto_renew) VALUES
    (2, 1, '2024-01-01 00:00:00', '2024-02-01 00:00:00', TRUE, FALSE);
    """
    await engine.execute(query)

async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
