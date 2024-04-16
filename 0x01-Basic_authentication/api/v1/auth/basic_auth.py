#!/usr/bin/env python3
"""Basic Auth module
"""
from api.v1.auth.auth import Auth


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
