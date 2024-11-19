#!/usr/bin/env python3
"""
Basic module to authenticate the API module
"""
import re
import base64
import binascii
from .auth import Auth
class BasicAuth(Auth):
    """
    BasicAuth class for handling basic authentication.
    """
    def extract_base64_authorization_header(
            self, 
            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header.
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')

        return None


    def decode_base64_authorization_header(self,
            base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header.
        """
        if isinstance(base64_authorization_header, str):
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None
