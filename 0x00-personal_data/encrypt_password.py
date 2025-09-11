#!/usr/bin/env python
"""
Encrypting passwords
"""
import bcrypt

def hash_password(password) -> bytes:
    """Hash a password string using bcrypt and return the hashed password as bytes"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
