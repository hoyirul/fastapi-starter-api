# sync/migrations/20241221082921_create_table_ref_user_companies.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "ref_user_companies"


async def upgrade(engine):
    await engine.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'refusercompanystatus') THEN
                CREATE TYPE RefUserCompanyStatus AS ENUM ('pending', 'approved', 'rejected');
            END IF;
        END $$;
        CREATE TABLE {table} (
            user_id BIGINT REFERENCES mst_users(id),
            company_id VARCHAR(10) REFERENCES mst_companies(id),
            status RefUserCompanyStatus DEFAULT 'pending',
            PRIMARY KEY (user_id, company_id)
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
