#!/usr/bin/env python3
"""
hash password
"""

import bcrypt


def hash_password(password):
    ''' Generate a salt and hash the password '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password


def is_valid(hashed_password, password):
    ''' Check if the password matches the hashed password '''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
