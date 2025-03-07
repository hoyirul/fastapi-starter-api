# sync/migrations/20241221082821_create_table_ref_user_permissions.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "ref_user_permissions"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            user_id BIGINT REFERENCES mst_users(id),
            permission_id BIGINT REFERENCES mst_permissions(id),
            PRIMARY KEY (user_id, permission_id)
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
