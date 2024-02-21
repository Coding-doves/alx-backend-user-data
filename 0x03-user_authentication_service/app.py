#!/usr/bin/env python3
''' flask app '''
from flask import Flask, jsonify, request, abort, redrect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index() -> str:
    ''' root endpoint '''
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    ''' POST/users '''
    email, password = request.form.get(email), request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
