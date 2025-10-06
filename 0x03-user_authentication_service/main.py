#!/usr/bin/env python
"""
Main test module for the authentication service
"""
import requests


BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    """Test registering a new user"""
    k = request.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
