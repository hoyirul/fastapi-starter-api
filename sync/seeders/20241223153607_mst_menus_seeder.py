# sync/seeders/mst_menus_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa
# With Hero Icons https://heroicons.com/outline

table = "mst_menus"


async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (parent_id, name, alias, link, icon, ordering) VALUES
    (NULL, 'Dashboard', 'group:dashboard', NULL, NULL, 1),

    (1, 'Users', 'group:users:users', '/users/users', 'UserIcon', 1),
    (1, 'Roles', 'group:users:roles', '/users/roles', 'UserPlusIcon', 2),
    (1, 'Permissions', 'group:users:permissions', '/users/permissions', 'UserCheckIcon', 3),
    (1, 'Access Menus', 'group:users:access-menus', '/users/access-menus', 'LockIcon', 4),

    (NULL, 'Audit Logs', 'group:audit-logs', NULL, 'FileTextIcon', 5),
    (6, 'Actions', 'group:audit-logs:actions', '/audit-logs/actions', 'NavigationIcon', 1),
    (6, 'Logs', 'group:audit-logs:logs', '/audit-logs/logs', 'ListIcon', 2);
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
