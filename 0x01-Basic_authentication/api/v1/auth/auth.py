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
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        path = path.rstrip('/') + '/'
        for exclusion_path in excluded_paths:
            if exclusion_path == path:
                return False
        

        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets the Authorization header field from the request.
        """
        if request is not None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Temporarily returns None, ignoring the request argument.
        """
        return None
