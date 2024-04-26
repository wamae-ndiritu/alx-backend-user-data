#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Save the user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(user)
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise ValueError("User with this email already exists")
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by a specified criteria

        Args:
            **kwargs: Arbitrary keyword arguments representing query criteria

        Returns:
            User: The first User object found matching the criteria

        Raises:
            NoResultFound: If no user matches the criteria
            InvalidRequestError: If wrong query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound as error:
            self._session.rollback()
            raise NoResultFound
        except InvalidRequestError as e:
            self._session.rollback()
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update the user specified

        Args:
            user_id (int): ID specifying the user to update
            **kwargs: Keyword arguments to be updated
        Raises:
            ValueError: If an argument does not correspond a user attribute
        Returns: None
        """
        user = self.find_user_by(id=user_id)

        for attr, value in kwargs.items():
            if hasattr(User, attr):
                setattr(user, attr, value)
            else:
                raise ValueError(f"Invalid attribute: {attr}")
        self._session.commit()
