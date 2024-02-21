#!/usr/bin/env python3
''' Hash password '''
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
        hashed_password = _hashed_password(password)
        return self._db.add_user(email, hashed_password)
