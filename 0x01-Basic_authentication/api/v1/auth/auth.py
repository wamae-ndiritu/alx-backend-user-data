#!/usr/bin/env python3
"""Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        If path is not in the list of strings
        excluded_paths return True
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        end_character = path[-1]
        new_path = ''
        if end_character == '/':
            return False
        else:
            new_path = path + '/'
        if new_path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the authorization headers
        """
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user
        """
        return None
