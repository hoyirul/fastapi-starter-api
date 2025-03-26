# src/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from fastapi import APIRouter
from src.modules.authentications.auth.routers import router as auth_router
from src.modules.authentications.roles.routers import router as role_router
from src.modules.authentications.permissions.routers import router as permission_router
from src.modules.authentications.users.routers import router as user_router
from src.modules.authentications.menus.routers import router as menu_router

# LOGS
from src.modules.logs.actions.routers import router as action_router
from src.modules.logs.audit_logs.routers import router as audit_log_router

# MASTER ACCOUNTS
from src.modules.masters.account_types.routers import router as account_type_router

routers = APIRouter()  # Test Commit

routers.include_router(auth_router, prefix=f"/auth", tags=["auth"])

# Permissions
routers.include_router(role_router, prefix=f"/access_controls/roles", tags=["roles"])
routers.include_router(
    permission_router, prefix=f"/access_controls/permissions", tags=["permissions"]
)

routers.include_router(user_router, prefix=f"/access_controls/users", tags=["users"])

# Menus
routers.include_router(menu_router, prefix=f"/access_controls/menus", tags=["menus"])

# Logs
routers.include_router(action_router, prefix=f"/logs/actions", tags=["actions"])
routers.include_router(
    audit_log_router, prefix=f"/logs/audit_logs", tags=["audit_logs"]
)

# Masters
routers.include_router(
    account_type_router, prefix=f"/masters/account_types", tags=["account_types"]
)