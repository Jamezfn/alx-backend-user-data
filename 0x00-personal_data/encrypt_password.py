#!/usr/bin/env python
"""
Encrypting passwords
"""
import bcrypt

def hash_password(password) -> bytes:
    """Hash a password string using bcrypt and return the hashed password as bytes"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
