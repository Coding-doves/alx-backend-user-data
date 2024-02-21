#!/usr/bin/env python3
''' Hash password '''
import uuid
from sqlalchemy.orm.exc import NoResultFound
from db import DB
import bcrypt
from uuid import uuid4
from user import User
from typing import Union


def _hash_password(password: str) -> bytes:
    ''' hashed paswd '''
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    ''' generate uuid '''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' register user '''
        user = self._db.find_user_by(email=email)
        if user is not None:
            raise ValueError(f"User {email} already exists")
        
        hashed_password = _hash_password(password)
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        ''' Valid login '''
        user = self._db.find_user_by(email=email)
        if user:
            _hash_password = user.hashed_password
            return bcrypt.checkpw(password.encode("utf-8"), _hash_password)
        return False

    def create_session(self, email: str) -> str:
        ''' create session '''
        usr = self._db.find_user_by(email=email)

        if usr:
            session_id = _generate_uuid()
            usr.session_id = session_id
            self._db.update_user(usr.id, session_id=session_id)
            return session_id
        return None
