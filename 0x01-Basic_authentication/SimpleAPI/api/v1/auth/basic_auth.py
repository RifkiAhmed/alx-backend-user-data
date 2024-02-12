#!/usr/bin/env python3
""" BasicAuth module
"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Returns a Base64 part of the Authorization header key
        """
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header.split(' ')[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a Base64 string
        """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            auth_decoded = base64.b64decode(base64_authorization_header)
            return auth_decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Returns the user email ans password
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':')
        if len(credentials) == 2:
            return tuple(credentials)
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ Returns the user instance based on the email and password
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if users:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request
        """
        authorization_header = self.authorization_header(request)
        if authorization_header:
            authorization_header = self.extract_base64_authorization_header(
                authorization_header)
            authorization_header = self.decode_base64_authorization_header(
                authorization_header)
            user_credentials = self.extract_user_credentials(
                authorization_header)
            user = self.user_object_from_credentials(
                user_credentials[0], user_credentials[1])
            return user
        return None
