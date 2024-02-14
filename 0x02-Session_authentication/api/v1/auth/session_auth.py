#!/usr/bin/env python3
""" SessionAuth module
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        """
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns a User instance based on a cookie value
        """
        _my_session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id=_my_session_id)
        try:
            return User.get(id=user_id)
        except KeyError:
            return None

    def destroy_session(self, request=None):
        """ Logout the user
        """
        if not request:
            return False
        _my_session_id = self.session_cookie(request)
        if not _my_session_id:
            return False
        del self.user_id_by_session_id[_my_session_id]
        return True
