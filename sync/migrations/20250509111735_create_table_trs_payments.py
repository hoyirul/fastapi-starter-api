
# sync/migrations/20250509111735_create_table_trs_payments.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "trs_payments"

async def upgrade(engine):
    await engine.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'trspaymentstatus') THEN
                CREATE TYPE TrsPaymentStatus AS ENUM ('pending', 'completed', 'failed');
            END IF;
        END $$;
        CREATE TABLE {table} (
            id varchar(50) PRIMARY KEY,
            user_id BIGINT REFERENCES mst_users(id),
            subscription_id BIGINT REFERENCES trs_subscriptions(id),
            subscription_plan_id BIGINT REFERENCES mst_subscription_plans(id),
            amount NUMERIC(10, 2) NOT NULL,
            payment_date TIMESTAMP NOT NULL,
            payment_method VARCHAR(50) NOT NULL,
            status TrsPaymentStatus DEFAULT 'pending'
        );
        """
    )

async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
