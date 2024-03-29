#!/usr/bin/env python3
""" Module of Session views """


from flask import jsonify, request, abort
from models.user import User
from typing import Tuple
from api.v1.views import app_views
from os import getenv


@app_views.route(
        '/auth_session/login',
        methods=["POST"],
        strict_slashes=False
        )
def user_login() -> Tuple[str, int]:
    ''' login authentication '''
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({"email": email})
    except Exception as e:
        return {"error": "no user found for this email"}, 404

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if user[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user[0].id)
        response = jsonify(user[0].to_json())
        response.set_cookie(getenv("SESSION_NAME"), session_id)
        return response, 200
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        "/auth_session/logout",
        methods=["DELETE"],
        strict_slashes=False
        )
def logout() -> Tuple[str, int]:
    ''' logout '''
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
