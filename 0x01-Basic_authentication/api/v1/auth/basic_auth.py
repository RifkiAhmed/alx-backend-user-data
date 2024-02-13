#!/usr/bin/env python3
""" BasicAuth module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header
        """
        if not isinstance(authorization_header, str):
            return None
        authorized_part = authorization_header.split(' ')
        if len(authorized_part) == 2 and authorized_part[0] == "Basic":
            return authorized_part[1]
        return None
