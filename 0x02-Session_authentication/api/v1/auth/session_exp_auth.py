#!/usr/bin/env python3
""" SessionExpAuth module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class
    """

    def __init__(self):
        """ Initialize a new SessionExpAuth instance
        """
        session_duration = os.getenv("SESSION_DURATION", "0")
        self.session_duration = int(session_duration)

    def create_session(self, user_id=None):
        """ Creates a Session ID for a user_id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID
        """
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_data = self.user_id_by_session_id[session_id]
        created_at = session_data.get("created_at")
        if not created_at:
            return None
        expiry_datetime = created_at + timedelta(seconds=self.session_duration)
        if self.session_duration > 0 and expiry_datetime < datetime.now():
            return None
        return session_data.get("user_id")
