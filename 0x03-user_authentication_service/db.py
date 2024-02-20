#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import Any
from user import Base, User


class DB:
    """ DB class
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
        """Add User object to the database
        Return
        - User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **key: Any) -> User:
        """Returns User object based on the key argument
        """
        user = self._session.query(User).filter_by(**key).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs: dict) -> User:
        """Updates a User object with the user_id
        """
        try:
            user = self.find_user_by(id=user_id)
            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
            return None
        except NoResultFound:
            return None
