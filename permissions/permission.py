# permissions/permission.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

import pandas as pd
# English
# Data permissions will be saved in the permissions.xlsx file
data = [
    ('manage:auth', 'Manage authentication permission'),
    ('switch:auth', 'Switch authentication permission'),
    ('manage:audit-logs', 'Manage audit logs permission'),
    ('view:audit-logs', 'View audit logs permission'),
    ('show:audit-logs', 'Show audit logs permission'),
    ('manage:users', 'Manage users permission'),
    ('view:users', 'View users permission'),
    ('show:users', 'Show users permission'),
    ('select:users', 'Select users permission'),
    ('create:users', 'Create users permission'),
    ('update:users', 'Update users permission'),
    ('assign:roles', 'Assign roles permission'),
    ('revoke:roles', 'Revoke roles permission'),
    ('grant:user-permissions', 'Assign permissions permission'),
    ('revoke:user-permissions', 'Revoke permissions permission'),
    ('inactive:users', 'Inactive users permission'),
    ('active:users', 'Active users permission'),
    ('manage:roles', 'Manage roles permission'),
    ('view:roles', 'View roles permission'),
    ('show:roles', 'Show roles permission'),
    ('select:roles', 'Select roles permission'),
    ('create:roles', 'Create roles permission'),
    ('update:roles', 'Update roles permission'),
    ('grant:role-permissions', 'Assign permissions permission'),
    ('revoke:role-permissions', 'Revoke permissions permission'),
    ('delete:roles', 'Delete roles permission'),
    ('trash:roles', 'Trash roles permission'),
    ('restore:roles', 'Restore roles permission'),
    ('manage:permissions', 'Manage permissions permission'),
    ('view:permissions', 'View permissions permission'),
    ('show:permissions', 'Show permissions permission'),
    ('select:permissions', 'Select permissions permission'),
    ('create:permissions', 'Create permissions permission'),
    ('update:permissions', 'Update permissions permission'),
    ('delete:permissions', 'Delete permissions permission'),
    ('trash:permissions', 'Trash permissions permission'),
    ('restore:permissions', 'Restore permissions permission'),
    ('manage:menus', 'Manage menus permission'),
    ('view:menus', 'View menus permission'),
    ('show:menus', 'Show menus permission'),
    ('select:menus', 'Select menus permission'),
    ('create:menus', 'Create menus permission'),
    ('update:menus', 'Update menus permission'),
    ('grant:role-menus', 'Assign menus permission'),
    ('revoke:role-menus', 'Revoke menus permission'),
    ('grant:user-menus', 'Assign menus permission'),
    ('revoke:user-menus', 'Revoke menus permission'),
    ('delete:menus', 'Delete menus permission'),
    ('trash:menus', 'Trash menus permission'),
    ('restore:menus', 'Restore menus permission'),
    ('hierarchy:menus', 'Hierarchy menus permission'),
    ('manage:actions', 'Manage actions permission'),
    ('view:actions', 'View actions permission'),
    ('show:actions', 'Show actions permission'),
    ('create:actions', 'Create actions permission'),
    ('update:actions', 'Update actions permission'),
    ('delete:actions', 'Delete actions permission'),
    ('trash:actions', 'Trash actions permission'),
    ('restore:actions', 'Restore actions permission'),
    ('color:actions', 'Color actions permission'),
    ('manage:account-types', 'Manage account types permission'),
    ('view:account-types', 'View account types permission'),
    ('show:account-types', 'Show account types permission'),
    ('select:account-types', 'Select account types permission'),
    ('create:account-types', 'Create account types permission'),
    ('update:account-types', 'Update account types permission'),
    ('delete:account-types', 'Delete account types permission'),
    ('trash:account-types', 'Trash account types permission'),
    ('restore:account-types', 'Restore account types permission')
]

# Compile the data into a DataFrame
df = pd.DataFrame(data, columns=['name', 'description'])

# Add an id column to the DataFrame
df['id'] = df.index + 1

# Reorder the columns
df = df[['id', 'name', 'description']]

# Save the data to an Excel file
file_path = './permissions/data/permissions.xlsx'
df.to_excel(file_path, index=False, engine='openpyxl')

print(f"Data berhasil disimpan ke {file_path}")
