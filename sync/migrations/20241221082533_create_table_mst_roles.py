# sync/migrations/20241221082533_create_table_mst_roles.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "mst_roles"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255),
            description TEXT
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
