#!/usr/bin/env python3
""" Module of Session views
"""
import uuid
from .auth import Auth


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
