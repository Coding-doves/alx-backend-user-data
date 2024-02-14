#!/usr/bin/env python3
""" basic_auth """
import re
from .auth import Auth


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
