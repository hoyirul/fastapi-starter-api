# sync/migrations/20241221082935_create_table_mst_account_types.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "mst_account_types"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
