#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hash password using bcrypt
    Args:
        password (str): The password to hash
    Returns:
        bytes: Hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """
        Instantiates Auth
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register user

        Args:
            email (str): User email
            password: User password
        Returns:
            User: The created User instance
        Raises:
            ValueError: If the user exist with the specified email
        """
        try:
            # Check email existence
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # No user, create new one
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
