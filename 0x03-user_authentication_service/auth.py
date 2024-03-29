#!/usr/bin/env python3
""" Auth model
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Returns a hashed password
    """
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash_password


def _generate_uuid() -> str:
    """Returns a string representation of the new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initializes a DB instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user into the database
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Checks user's credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode("utf-8"),
                user.hashed_password)
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """Returns user's session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns a user based on it's session id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session
        """
        try:
            user = self._db.find_user_by(id=user_id)
            return self._db.update_user(user.id, session_id=None)
        except (NoResultFound, InvalidRequestError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_password = _hash_password(password)
            return self._db.update_user(
                user.id, hashed_password=hash_password, reset_token=None)
        except (NoResultFound, InvalidRequestError):
            raise ValueError
