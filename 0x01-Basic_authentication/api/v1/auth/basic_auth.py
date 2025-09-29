#!/usr/bin/env python
""" BasicAuth module
"""

from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar

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

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """"""
        if user_email is None or  not isinstance(user_email, str):
            return None

        if user_pwd is None or  not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except DatabaseError as e:
            return None

        if not users or len(users) == 0:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the User instance for a request using Basic Auth."""
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        b64_part = self.extract_base64_authorization_header(auth_header)
        if b64_part is None:
            return None

        decoded = self.decode_base64_authorization_header(b64_part)
        if decoded is None:
            return None

        email, pwd = self.extract_user_credentials(decoded)
        if email is None or pwd is None:
            return None

        return self.user_object_from_credentials(email, pwd)
