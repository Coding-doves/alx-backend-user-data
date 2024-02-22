#!/usr/bin/env python3
''' flask app '''
from flask import Flask, jsonify, request, abort, redirect

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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    ''' POST/sessions '''
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res
    

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    ''' DELETE/sessions '''
    ses_id = request.cookies.get("session_id")
    usr = AUTH.get_user_from_session_id(ses_id)
    if usr is None:
        abort(403)
    AUTH.destroy_session(usr.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    ''' GET/profile '''
    ses_id = request.cookies.get("session_id")
    usr = AUTH.get_user_from_session_id(ses_id)
    if usr is None:
        abort(403)
    return jsonify({"email": usr.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    ''' POST/reset_password '''
    email = request.form.get(email)
    reset_token = None
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
        
    if reset_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    ''' PUT/reset_password '''
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    password_changed = False
    
    try:
        Auth.update_password(reset_token, new_password)
        password_changed = True
    except ValueError:
        password_changed = False
    if not password_changed:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
