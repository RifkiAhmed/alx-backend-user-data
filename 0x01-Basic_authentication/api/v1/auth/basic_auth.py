#!/usr/bin/env python3
""" BasicAuth module
"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of the Base64 string
        """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_authorized_header = base64.b64decode(
                base64_authorization_header
            )
            return decoded_authorized_header.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
