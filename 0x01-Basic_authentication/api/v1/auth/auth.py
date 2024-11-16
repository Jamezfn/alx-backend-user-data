#!/usr/bin/env python3
"""
Authentification module for the API
"""
from typing import List, TypeVar
from flask import request
import re

class Auth:
    """
    Authentification class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentification
        
        if path is None or excluded_paths is None:
            return True

        path = path.rstrip('/')
        for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                exclusion_path = exclusion_path.rstrip('/')

                if exclusion_path.endswith('*'):
                    if path.startswith(exclusion_path[:-1]):
                        return False
                elif path == exclusion_path:
                    return False
        """

        return False

    def authorization_header(self, request=None) -> str:
        """
        Temporarily returns None, ignoring the request argument.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Temporarily returns None, ignoring the request argument.
        """
        return None
