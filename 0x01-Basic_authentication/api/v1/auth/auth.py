#!/usr/bin/env python3
""" Module for auth
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """ Manage API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user
        """
        return None
