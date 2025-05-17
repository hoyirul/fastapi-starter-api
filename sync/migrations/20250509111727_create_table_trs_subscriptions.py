
# sync/migrations/20250509111727_create_table_trs_subscriptions.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "trs_subscriptions"

async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES mst_users(id),
            subscription_plan_id BIGINT REFERENCES mst_subscription_plans(id),
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            auto_renew BOOLEAN DEFAULT FALSE
        );
        """
    )

async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
