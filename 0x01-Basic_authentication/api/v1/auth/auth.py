#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path is not in excluded paths else False
        """
        if path and not path.endswith('/'):
            path += "/"
        if path in excluded_paths:
            return False
        return False

    def authorization_header(self, request=None) -> str:
        """ Return None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return None
        """
        return None
