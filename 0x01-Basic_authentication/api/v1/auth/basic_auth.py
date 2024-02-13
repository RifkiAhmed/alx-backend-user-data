#!/usr/bin/env python3
""" BasicAuth module
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


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

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Returns the user email and password from the Base64 decoded value
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        user_credentials = decoded_base64_authorization_header.split(':')
        if len(user_credentials) == 2:
            return (user_credentials[0], user_credentials[1])
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if not (isinstance(user_email, str) and isinstance(user_pwd, str)):
            return None
        try:
            users = User.search(attributes={"email": user_email})
            if users:
                for user in users:
                    if user.is_valid_password(pwd=user_pwd):
                        return user
            return None
        except Exception:
            return None
