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
    """Logout endpoint - destroys session and redirects home"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")

@app.route("/profile", methods=["GET"], strict_slashes=True)
def profile():
    """Return the email of the logged-in user based on session cookie."""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})

@app.route("/reset_password", methods=["POST"], strict_slashes=True)
def reset_password():
    """Handle reset password token request"""
    email = request.form.get("email")
    if email is None:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200

@app.route("/reset_password", methods=["PUT"], strict_slashes=True)
def update_password():
    """Handle password update using reset token."""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if email is None or reset_token is None or new_password is None:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True, use_reloader=True)
