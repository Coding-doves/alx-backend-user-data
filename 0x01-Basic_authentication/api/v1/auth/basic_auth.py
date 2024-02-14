#!/usr/bin/env python3
""" basic_auth """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    ''' inherit from Auth class '''
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        ''' extract '''
        if authorization_header is None:
            return None
        if authorization_header is not 
