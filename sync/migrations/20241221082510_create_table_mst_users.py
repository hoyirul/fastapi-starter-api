# sync/migrations/20241221082510_create_table_mst_users.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "mst_users"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255),
            active BOOLEAN DEFAULT TRUE,
            last_logged_in TIMESTAMP DEFAULT NULL
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
