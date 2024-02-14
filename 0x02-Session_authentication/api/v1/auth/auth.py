#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path is not in excluded paths else False
        """
        if path and not path.endswith('/'):
            path += "/"
        if excluded_paths and path in excluded_paths:
            return False
        if excluded_paths and any(excluded_path.endswith('*')
                                  and path.startswith(excluded_path[:-1])
                                  for excluded_path in excluded_paths):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Return the request header key Authorization value
        """
        if request:
            authorization_header = request.headers.get("Authorization")
            if authorization_header:
                return authorization_header
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return None
        """
        return None

    def session_cookie(self, request=None) -> str:
        """ Returns a cookie value from a request
        """
        if not request:
            return None
        _my_cookie_name = os.getenv("SESSION_NAME")
        _my_session_id = request.cookies.get(_my_cookie_name)
        return _my_session_id
