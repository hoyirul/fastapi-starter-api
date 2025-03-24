# sync/migrations/20241221082754_create_table_ref_role_menus.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "ref_role_menus"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            role_id BIGINT REFERENCES mst_roles(id),
            menu_id BIGINT REFERENCES mst_menus(id),
            PRIMARY KEY (role_id, menu_id)
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
