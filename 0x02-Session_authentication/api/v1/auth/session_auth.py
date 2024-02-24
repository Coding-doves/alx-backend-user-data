#!/usr/bin/env python3
""" Module of Session views
"""
import uuid
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    ''' Session views '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' create session '''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_ID = str(uuid.uuid4())
        self.user_id_by_session_id[session_ID] = user_id
        return session_ID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' user id session id '''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        ''' returns User'''
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    """ def destroy_session(self, request=None) -> bool:
        ''' logout and destory '''
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user = self.user_id_by_session_id(session_id)
        if user is not None:
            del self.user_id_by_session_id[session_id]
            return True

        return False """
    def destroy_session(self, request=None):
        """ destoy sessions """
        session_id = self.session_cookie(request)
        user = self.user_id_for_session_id(session_id)
        if ((request is None or session_id is None) or
                user is None):
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
