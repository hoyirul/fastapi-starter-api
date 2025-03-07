# sync/migrations/20241221082814_create_table_ref_user_roles.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "ref_user_roles"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            user_id BIGINT REFERENCES mst_users(id),
            role_id BIGINT REFERENCES mst_roles(id),
            PRIMARY KEY (user_id, role_id)
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
