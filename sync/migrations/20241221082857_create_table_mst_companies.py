# sync/migrations/20241221082857_create_table_mst_companies.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "mst_companies"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255),
            address TEXT,
            contact_email VARCHAR(255)
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
