
# sync/seeders/mst_subscription_plans_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "mst_subscription_plans"

async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (name, price, billing_cycle, category, description) VALUES
    ('Free Plan', 0.00, 'monthly', 0, 'Free plan with limited features'),
    ('Basic Plan', 9.99, 'monthly', 1, 'Basic plan with essential features'),
    ('Pro Plan', 19.99, 'monthly', 1, 'Pro plan with advanced features'),
    ('Enterprise Plan', 49.99, 'monthly', 1, 'Enterprise plan with all features and support'),
    ('Basic Yearly Plan', 99.99, 'yearly', 1, 'Basic yearly plan with essential features'),
    ('Pro Yearly Plan', 199.99, 'yearly', 1, 'Pro yearly plan with advanced features'),
    ('Enterprise Yearly Plan', 499.99, 'yearly', 1, 'Enterprise yearly plan with all features and support'),
    ('Token Plan', 0.00, 'monthly', 2, 'Token plan for additional features');
    """
    await engine.execute(query)

async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
