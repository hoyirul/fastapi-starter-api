# src/databases/redis.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

import redis
from src.configs import Config

JTI_EXPIRY = 3600

token_blocklist = redis.Redis(
    host=Config.DB_REDIS_HOST,
    port=Config.DB_REDIS_PORT,
    db=0,
    decode_responses=True,
)


class RedisDB:
    async def add_jti_to_blocklist(self, jti: str) -> None:
        token_blocklist.set(jti, "", ex=JTI_EXPIRY)

    async def token_in_blocklist(self, jti: str) -> bool:
        return token_blocklist.get(jti) is not None

    async def clear_blocklist(self) -> None:
        token_blocklist.flushdb()

    async def is_connected(self) -> bool:
        try:
            token_blocklist.ping()
            return True
        except redis.ConnectionError:
            return False
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to connect to Redis: {e}"
            )
