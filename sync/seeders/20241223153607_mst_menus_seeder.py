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
    (1, 'Profit & Loss', 'group:dashboard:profit-and-loss', '/profit-and-loss', 'PieChartIcon', 1),
    (1, 'Balance Sheet', 'group:dashboard:balance-sheet', '/balance-sheet', 'BarChartIcon', 2),

    (NULL, 'Journals', 'group:journals', NULL, NULL, 2),
    (4, 'Journal Entries', 'group:journals:journal-entries', '/journals/journal-entries', 'FilePlusIcon', 1),
    (4, 'Cash Funds', 'group:journals:cash-funds', '/journals/cash-funds', 'DollarSignIcon', 2),

    (4, 'Chart of Accounts', 'group:journals:coa', NULL, 'BarChart2Icon', 3),
    (7, 'COA', 'group:journals:coa:coa', '/journals/coa', 'ExternalLinkIcon', 1),
    (7, 'Hierarchy', 'group:journals:coa:hierarchy', '/journals/hierarchy', 'GitPullRequestIcon', 2),
    
    (NULL, 'Others', 'group:others', NULL, NULL, 3),

    (10, 'Journals', 'group:journals', NULL, 'DatabaseIcon', 1),
    (11, 'Journals', 'group:journals:journals', '/journals/journals', 'HardDriveIcon', 1),
    (11, 'Journal Types', 'group:journals:journal-types', '/journals/journal-types', 'GlobeIcon', 2),

    (10, 'Accounts', 'group:accounts', NULL, 'FolderIcon', 2),
    (14, 'Accounts', 'group:accounts:accounts', '/accounts/accounts', 'ShoppingBagIcon', 1),
    (14, 'Account Types', 'group:accounts:account-types', '/accounts/account-types', 'Columns2Icon', 2),
    (14, 'Account Categories', 'group:accounts:account-categories', '/accounts/account-categories', 'FilterIcon', 3),
    (14, 'Account Tags', 'group:accounts:account-tags', '/accounts/account-tags', 'TagIcon', 4),
    (14, 'Account Levels', 'group:accounts:account-levels', '/accounts/account-levels', 'SlidersIcon', 5),
    (14, 'Analytic Accounts', 'group:accounts:analytic-accounts', '/accounts/analytic-accounts', 'MonitorIcon', 6),

    (10, 'Transactions', 'group:transactions', NULL, 'PieChartIcon', 3),
    (21, 'Currencies', 'group:transactions:currencies', '/transactions/currencies', 'DollarSignIcon', 1),
    (21, 'Taxes', 'group:transactions:taxes', '/transactions/taxes', 'PrinterIcon', 2),

    (10, 'User & Permissions', 'group:users', NULL, 'UsersIcon', 4),
    (24, 'Users', 'group:users:users', '/users/users', 'UserIcon', 1),
    (24, 'Roles', 'group:users:roles', '/users/roles', 'UserPlusIcon', 2),
    (24, 'Permissions', 'group:users:permissions', '/users/permissions', 'UserCheckIcon', 3),
    (24, 'Access Menus', 'group:users:access-menus', '/users/access-menus', 'LockIcon', 4),

    (10, 'Audit Logs', 'group:audit-logs', NULL, 'FileTextIcon', 5),
    (29, 'Actions', 'group:audit-logs:actions', '/audit-logs/actions', 'NavigationIcon', 1),
    (29, 'Logs', 'group:audit-logs:logs', '/audit-logs/logs', 'ListIcon', 2);
    """
    await engine.execute(query)


async def rollback(engine):
    f"""Clear all data from {table} table"""
    query = f"TRUNCATE TABLE {table};"
    await engine.execute(query)
