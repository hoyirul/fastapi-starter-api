# src/utils/chiper.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib
from .logging import Logging

logger = Logging(level="DEBUG")


# For encrypting and decrypting password
def encrypt_password(password: str, key: str):
    try:
        # Convert the key from hexadecimal string to bytes
        key_bytes = bytes.fromhex(key)

        iv = os.urandom(16)  # Generate a random IV (Initialization Vector)
        cipher = Cipher(
            algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()

        # Apply padding to ensure the data length is a multiple of AES block size (16 bytes)
        padding_length = 16 - (len(password) % 16)
        password_padded = password + chr(padding_length) * padding_length

        encrypted_password = (
            encryptor.update(password_padded.encode()) + encryptor.finalize()
        )

        # Combine IV with the encrypted data and convert to hexadecimal format
        encrypted_password_hex = (iv + encrypted_password).hex()
        return encrypted_password_hex
    except Exception as e:
        logger.log("error", f"Encryption failed: {e}")
        return None


# Decrypt password
def decrypt_password(encrypted_password_hex: str, key_hex: str):
    try:
        # Convert the key from hexadecimal string to bytes
        key = bytes.fromhex(key_hex)

        # Convert the encrypted password from hexadecimal string to bytes
        encrypted_password = bytes.fromhex(encrypted_password_hex)

        iv = encrypted_password[:16]  # Extract IV from the first 16 bytes
        encrypted_password = encrypted_password[
            16:
        ]  # Extract the encrypted password data

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()

        # Remove padding
        padding_length = ord(decrypted_password[-1:])
        return decrypted_password[:-padding_length].decode()
    except Exception as e:
        logger.log("error", f"Decryption failed: {e}")
        return None


# Generate 32-byte key from a string
def generate_key(password: str) -> bytes:
    try:
        # Use SHA-256 to generate 32-byte key
        return hashlib.sha256(password.encode()).digest()
    except Exception as e:
        logger.log("error", f"Key generation failed: {e}")
        return None
