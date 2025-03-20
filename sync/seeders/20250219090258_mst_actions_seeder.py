
# sync/seeders/mst_actions_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "mst_actions"

async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (name, description, color)
    VALUES
    ('CREATE', 'Create a new record', 'green'),
    ('UPDATE', 'Update an existing record', 'sky'),
    ('DELETE', 'Delete an existing record', 'rose'),
    ('RESTORE', 'Restore a trashed record', 'slate'),
    ('POST', 'Post a existing record for journal etc', 'blue'),
    ('UNPOST', 'Post a existing record for journal etc', 'gray'),
    ('PUBLISH' , 'Publish a existing record', 'violet'),
    ('UNPUBLISH', 'Publish a existing record', 'yellow'),
    ('APPROVE', 'Approve a existing record', 'orange'),
    ('REJECT', 'Reject a existing record', 'red'),
    ('LOGIN', 'Login to the system', 'emerald'),
    ('LOGOUT', 'Logout from the system', 'fuchsia');
    """
    await engine.execute(query)

async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
