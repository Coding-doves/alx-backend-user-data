#!/usr/bin/env python3
""" auth """

from flask import request
from typing import List, TypeVar


class Auth:
    """ auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' require_auth '''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        path = path.rstrip("/")

        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip("/")
            if (excluded_path.endswith("*") and
                    path.startswith(excluded_path[:-1])):
                return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' authorization_header '''
        if request is None:
            return None

        header = request.headers.get("Authorization", None)
        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        ''' current_user '''
        return None
