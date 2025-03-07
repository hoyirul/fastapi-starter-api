# src/utils/security.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

"""
This module contains security-related functions such as password hashing, password verification, token generation, and token verification.
DON'T MODIFY THIS FILE!
"""

from fastapi import status
import bcrypt
import base64
import jwt
from datetime import timedelta, datetime
from src.configs import Config
import uuid
import logging
from fastapi.exceptions import HTTPException


# Hash a password using bcrypt
def password_hash(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    # Mengonversi hasil hash menjadi base64 string agar bisa disimpan di database
    return base64.b64encode(hashed_password).decode("utf-8")


# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode("utf-8")
    hashed_password_bytes = base64.b64decode(hashed_password)  # Decode kembali ke bytes
    return bcrypt.checkpw(
        password=password_byte_enc, hashed_password=hashed_password_bytes
    )


def generate_token(data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload["user"] = data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=Config.JWT_EXPIRY)
    )

    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    access_token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM,
    )

    return access_token


def verify_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
            options={"verify_exp": True},
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        logging.exception(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={
                "message": "Token is expired",
                "resolution": "Please get new token",
                "error_code": "token_expired",
            }
        )
    except jwt.InvalidTokenError as e:
        logging.exception(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        )
    except Exception as e:
        logging.exception(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        )
