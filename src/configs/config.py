# src/modules/configs/config.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

"""
This module is used to store the configuration of the application.
DON'T CHANGE ANYTHING IN THIS FILE UNLESS YOU KNOW WHAT YOU'RE DOING.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from src.utils.chiper import decrypt_password
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints."
    )
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: str = 8000

    SECRET_KEY: str = "secret"

    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY: int = 3600  # seconds
    JWT_REFRESH_EXPIRY: int = 172800  # seconds / 2 days

    DB_REDIS_HOST: str = "localhost"
    DB_REDIS_PORT: int = 6379
    DB_REDIS_PASSWORD: str = "secret"

    DB_SECRET_KEY: str = "secret"
    DB_DRIVER: str = "asyncpg"
    DB_CONNECTION: str = "postgresql"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "db"
    DATABASE_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


Config = Settings()

# Decrypt the database password
Config.DB_REDIS_PASSWORD = decrypt_password(
    Config.DB_REDIS_PASSWORD, Config.DB_SECRET_KEY
)
Config.DB_PASSWORD = decrypt_password(Config.DB_PASSWORD, Config.DB_SECRET_KEY)
Config.DATABASE_URL = f"{Config.DB_CONNECTION}+{Config.DB_DRIVER}://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
