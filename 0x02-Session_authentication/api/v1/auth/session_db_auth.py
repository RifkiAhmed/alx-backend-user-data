#!/usr/bin/env python3
""" SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """

    def create_session(self, user_id=None):
        """ Creates and stores new instance of UserSession
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the User ID by requesting UserSession
        in the database based on session_id
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_sessions = None
        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        if not user_sessions:
            return None
        user_id = user_sessions[0].user_id
        if self.session_duration <= 0:
            return user_id
        created_at = user_sessions[0].created_at
        if not created_at:
            return None
        expiry_datetime = created_at + timedelta(seconds=self.session_duration)
        if expiry_datetime < datetime.utcnow():
            return None
        return user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID
        from the request cookie
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        UserSession.load_from_file()
        try:
            user_sessions = UserSession.search({"session_id": session_id})
            if not user_sessions:
                return False
            user_sessions[0].remove()
            return True
        except KeyError:
            return False
