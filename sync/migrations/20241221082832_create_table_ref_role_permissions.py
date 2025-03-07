# sync/migrations/20241221082832_create_table_ref_role_permissions.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "ref_role_permissions"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            role_id BIGINT REFERENCES mst_roles(id),
            permission_id BIGINT REFERENCES mst_permissions(id),
            PRIMARY KEY (role_id, permission_id)
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
