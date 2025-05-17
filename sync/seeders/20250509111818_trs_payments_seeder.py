
# sync/seeders/trs_payments_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "trs_payments"

async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (id, user_id, subscription_id, subscription_plan_id, amount, payment_date, payment_method, status) VALUES
    ('pay_1', 2, 1, 1, 9.99, '2024-01-01 00:00:00', 'credit_card', 'completed');
    """
    await engine.execute(query)

async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
