#!/usr/bin/env python
""" BasicAuth module
"""

from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """ BasicAuth inherits from Auth """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """"""
        if authorization_header is None or not isinstance(authorization_header, str) or not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split()[1]
