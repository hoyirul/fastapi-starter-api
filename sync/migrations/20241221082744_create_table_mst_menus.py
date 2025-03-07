# sync/migrations/20241221082744_create_table_mst_menus.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "mst_menus"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            id BIGSERIAL PRIMARY KEY,
            parent_id BIGINT REFERENCES mst_menus(id),
            name VARCHAR(255),
            alias VARCHAR(255),
            link VARCHAR(255),
            icon VARCHAR(255),
            ordering INT
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
