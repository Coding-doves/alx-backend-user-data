#!/usr/bin/env python3
""" basic_auth """
import re
from .auth import Auth
import base64
import binascii
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    ''' inherit from Auth class '''
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        ''' extract '''
        if authorization_header is None:
            return None
        if type(authorization_header) == str:
            pat = r'Basic (?P<token>.+)'
            match = re.fullmatch(pat, authorization_header.strip())
            if match is not None:
                return match.group('token')
            return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """ decode """
        if type(base64_authorization_header) == str:
            try:
                result = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return result.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """
            extract user credentials from the base64-decoded
            authorization header module
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if match is not None:
                user = match.group('user')
                password = match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ user authentication """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                user = User.search({'email': user_email})
            except Exception:
                return None
            if not user:
                return None
            # if len(user) <= 0:
                # return None
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ complete Basic authentication """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
