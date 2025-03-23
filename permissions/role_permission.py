
# permissions/role_permission.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

import pandas as pd

# Reading the permissions.xlsx file
permissions_df = pd.read_excel('./permissions/data/permissions.xlsx', engine='openpyxl')

# Adding a 'permission_id' column to permissions (for permission_id)
permissions_df['permission_id'] = permissions_df.index + 1

# Filtering permissions that start with 'manage:'
manage_permissions = permissions_df[permissions_df['name'].str.startswith('manage:')]

# Role and role_id mapping
roles = {
    1: "Super Admin",
    2: "Admin",
    3: "Accountant",
    4: "Finance",
    5: "Tax Officer",
    6: "User"
}

# Creating a mapping between role_id and permission_id
role_permissions = {
    1: [],  # Super Admin
    2: [],  # Admin
    3: [],  # Accountant
    4: [],  # Finance
    5: [],  # Tax Officer
    6: []   # User
}

# Super Admin: get all manage: permissions and others
for permission_id in manage_permissions['permission_id']:
    role_permissions[1].append(permission_id)  # Super Admin gets all manage: permissions

# Admin: access to 'manage:auth', 'manage:users', 'view:roles'
role_permissions[2].append(1)  # Admin gets access to 'manage:auth'
role_permissions[2].append(3)  # Admin gets access to 'manage:users'
role_permissions[2].append(9)  # Admin gets access to 'view:roles'

# Accountant: access to 'view:transactions', 'view:accounts', 'view:journal-entries'
role_permissions[3].append(4)  # Accountant gets access to 'view:users'
role_permissions[3].append(8)  # Accountant gets access to 'view:transactions'
role_permissions[3].append(5)  # Accountant gets access to 'view:accounts'

# Finance: access to 'view:accounts', 'manage:accounts', 'create:accounts'
role_permissions[4].append(5)  # Finance gets access to 'view:accounts'
role_permissions[4].append(6)  # Finance gets access to 'manage:accounts'
role_permissions[4].append(7)  # Finance gets access to 'create:accounts'

# Tax Officer: access to 'view:taxes', 'manage:taxes', 'create:taxes'
role_permissions[5].append(10)  # Tax Officer gets access to 'view:taxes'
role_permissions[5].append(11)  # Tax Officer gets access to 'manage:taxes'
role_permissions[5].append(12)  # Tax Officer gets access to 'create:taxes'

# User: access to 'view:users', 'view:transactions'
role_permissions[6].append(4)  # User can access 'view:users'
role_permissions[6].append(8)  # User can access 'view:transactions'

# Save the role_permissions data into an Excel file with sheets per role
with pd.ExcelWriter('./permissions/data/role_permissions.xlsx', engine='openpyxl') as writer:
    for role_id, permissions in role_permissions.items():
        role_name = roles[role_id]
        
        # Create DataFrame for role_permissions
        role_permissions_df = pd.DataFrame({
            'role_id': [role_id] * len(permissions),
            'permission_id': permissions
        })
        
        # Write DataFrame to Excel
        role_permissions_df.to_excel(writer, sheet_name=role_name, index=False)

df = pd.read_excel('./permissions/data/role_permissions.xlsx', sheet_name='Super Admin')
for _, data in df.iterrows():  # `iterrows()` for iterating over the rows of the DataFrame
    print(f"({data['role_id']}, {data['permission_id']}),")

print("Role permissions data successfully saved to role_permissions.xlsx with sheets per role.")
