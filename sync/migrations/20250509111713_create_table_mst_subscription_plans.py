
# sync/migrations/20250509111713_create_table_mst_subscription_plans.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "mst_subscription_plans"

async def upgrade(engine):
    await engine.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'mstsubscriptionplanbillingcycle') THEN
                CREATE TYPE MstSubscriptionPlanBillingCycle AS ENUM ('monthly', 'yearly');
            END IF;
        END $$;
        CREATE TABLE {table} (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255),
            price NUMERIC(10, 2),
            billing_cycle MstSubscriptionPlanBillingCycle DEFAULT 'monthly',
            category INTEGER default 0,
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
