# sync/migrations/20241221082843_create_table_audit_logs.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

table = "audit_logs"


async def upgrade(engine):
    await engine.execute(
        f"""
        CREATE TABLE {table} (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES mst_users(id),
            action_id BIGINT REFERENCES mst_actions(id),
            record_id VARCHAR(30) NOT NULL,
            ip_address VARCHAR(20) NOT NULL,
            model_name VARCHAR(100) NOT NULL,
            notes TEXT DEFAULT NULL,
            actioned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )


async def downgrade(engine):
    await engine.execute(
        f"""
        DROP TABLE {table};
        """
    )
