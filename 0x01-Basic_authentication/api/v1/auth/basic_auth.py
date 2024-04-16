#!/usr/bin/env python3
"""Basic Auth module
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Implements Basic Auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract base64 authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the Base64 encoded str
            decoded_bytes = base64.b64decode(
                    base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Extract user credentials from
        the decoded base64 authorization headers
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(
                decoded_base64_authorization_header,
                str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """
        Returns User instance based on his email
        and password
        """
        if user_email is None or not isinstance(
                user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user in the db
        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request
        """
        auth_headers = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
                auth_headers
                )
        decoded_str = self.decode_base64_authorization_header(
                base64_auth_header)
        email, pwd = self.extract_user_credentials(decoded_str)
        user = self.user_object_from_credentials(email, pwd)
        return user
