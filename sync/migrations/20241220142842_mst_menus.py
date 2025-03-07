# sync/migrations/20241220142842_create_mst_menus_table.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "mst_menus"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            id BIGSERIAL PRIMARY KEY,
            parent_id BIGINT REFERENCES {table}(id) DEFAULT NULL,
            name VARCHAR(255) NOT NULL,
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
