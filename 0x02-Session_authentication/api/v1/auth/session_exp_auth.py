#!/usr/bin/env python3
''' expiry session '''
from flask import request
from datetime import datetime, timedelta
from .session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    ''' session timeout '''
    def __init__(self) -> None:
        """ constructor """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ creates new session """
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now(),
            }
            return session_id
        else:
            return None

    def user_id_for_session_id(self, session_id=None) -> str:
        """ gets user id using the session id """
        if session_id in self.user_id_by_session_id:
            session = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session["user_id"]

            if "created_at" in session:
                current_time = datetime.now()
                time = timedelta(seconds=self.session_duration)
                expire_date = session["created_at"] + time
            else:
                return None

            if expire_date < current_time:
                return None

            return session["user_id"]
