#!/usr/bin/env python
"""
"""
from flask import Flask, request, jsonify, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=["GET"], strict_slashes=True)
def index():
    """Return a simple JSON payload"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=True)
def users():
    """Register a new user using form data 'email' and 'password'."""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"], strict_slashes=True)
def login():
    """"""
    email =  request.form.get("email")
    password = request.form.get("password")
    
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(401)

    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id, path="/")
    return resp

@app.route("/sessions", methods=["DELETE"], strict_slashes=True)
def logout():
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(401)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(401)

    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
