# sync/migrations/20241221082800_create_table_ref_user_menus.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

table = "ref_user_menus"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            user_id BIGINT REFERENCES mst_users(id),
            menu_id BIGINT REFERENCES mst_menus(id),
            PRIMARY KEY (user_id, menu_id)
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
