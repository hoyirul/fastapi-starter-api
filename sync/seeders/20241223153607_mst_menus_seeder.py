# sync/seeders/mst_menus_seeder.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah
# With Hero Icons https://heroicons.com/outline

table = "mst_menus"


async def seed(engine):
    f"""Insert initial data into {table} table"""
    query = f"""
    INSERT INTO {table} (parent_id, name, alias, link, icon, ordering) VALUES
    (NULL, 'Dashboard', 'group:dashboard', NULL, NULL, 1),
    (1, 'Profit & Loss', 'group:dashboard:profit-and-loss', '/profit-and-loss', 'presentation-chart-bar', 1),
    (1, 'Balance Sheet', 'group:dashboard:balance-sheet', '/balance-sheet', 'presentation-chart-line', 2),

    (NULL, 'Journals', 'group:journals', NULL, NULL, 2),
    (4, 'Journal Entries', 'group:journals:journal-entries', '/journals/journal-entries', 'credit-card', 1),
    (4, 'Cash Funds', 'group:journals:cash-funds', '/journals/cash-funds', 'fa receipt-refund', 2),

    (4, 'Chart of Accounts', 'group:journals:coa', NULL, 'newspaper', 3),
    (7, 'COA', 'group:journals:coa:coa', '/journals/coa', NULL, 1),
    (7, 'Hierarchy', 'group:journals:coa:hierarchy', '/journals/hierarchy', NULL, 2),
    
    (NULL, 'Others', 'group:others', NULL, NULL, 3),

    (10, 'Journal Types', 'group:journals', NULL, 'wrench-screwdriver', 1),
    (12, 'Journals', 'group:journals:journals', '/journals/journals', NULL, 1),
    (12, 'Journal Types', 'group:journals:journal-types', '/journals/journal-types', NULL, 2),

    (10, 'Accounts', 'group:accounts', NULL, 'adjustments-horizontal', 2),
    (15, 'Accounts', 'group:accounts:accounts', '/accounts/accounts', NULL, 1),
    (15, 'Account Types', 'group:accounts:account-types', '/accounts/account-types', NULL, 2),
    (15, 'Account Categories', 'group:accounts:account-categories', '/accounts/account-categories', NULL, 3),
    (15, 'Account Tags', 'group:accounts:account-tags', '/accounts/account-tags', NULL, 4),
    (15, 'Account Levels', 'group:accounts:account-levels', '/accounts/account-levels', NULL, 5),
    (15, 'Analytic Accounts', 'group:accounts:analytic-accounts', '/accounts/analytic-accounts', NULL, 6),

    (10, 'Transactions', 'group:transactions', NULL, 'banknotes', 3),
    (22, 'Currencies', 'group:transactions:currencies', '/transactions/currencies', NULL, 1),
    (22, 'Taxes', 'group:transactions:taxes', '/transactions/taxes', NULL, 2),

    (10, 'User & Permissions', 'group:users', NULL, 'cog', 4),
    (25, 'Users', 'group:users:users', '/users/users', NULL, 1),
    (25, 'Roles', 'group:users:roles', '/users/roles', NULL, 2),
    (25, 'Permissions', 'group:users:permissions', '/users/permissions', NULL, 3),
    (25, 'Access Menus', 'group:users:access-menus', '/users/access-menus', NULL, 4),

    (10, 'Audit Logs', 'group:audit-logs', NULL, 'computer-desktop', 5),
    (30, 'Actions', 'group:audit-logs:actions', '/audit-logs/actions', NULL, 1),
    (30, 'Logs', 'group:audit-logs:logs', '/audit-logs/logs', NULL, 2);
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
