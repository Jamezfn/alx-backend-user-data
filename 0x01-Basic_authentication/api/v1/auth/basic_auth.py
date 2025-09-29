#!/usr/bin/env python
""" BasicAuth module
"""

from api.v1.auth.auth import Auth
import base64

class BasicAuth(Auth):
    """ BasicAuth inherits from Auth """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header for Basic Authentication."""
        if authorization_header is None or not isinstance(authorization_header, str) or not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes a Base64 string and returns the UTF-8 value."""
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_bytes = base64.b64decode(base64_authorization_header, validate=True)
            return decode_bytes.decode("utf-8")
        except base64.binascii.Error:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """"""
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str) or ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
