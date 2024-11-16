#!/usr/bin/env python3
"""
Authentification module for the API
"""
from typing import List
from flask import request

class Auth:
    """
    Authentification class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentification
        """
        if path is not None and excluded_paths is not None:
            for exclusive_path in map(lambda x: x.strip(), exclude_paths):
                pattern = ""
                if exclusive_path[-1] == '*':
        return True
    def authorization_header(self, request=None) -> str:
