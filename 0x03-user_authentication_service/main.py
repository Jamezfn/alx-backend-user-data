#!/usr/bin/env python
"""
Main test module for the authentication service
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    """Test registering a new user"""
    k = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert k.status_code == 200, f"Unexpected status {k.status_code}"
    assert k.json() == {"email": email, "message": "user created"}
    print("register_user: OK")

def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password"""
    k = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert k.status_code == 401, f"Expected 401, got {k.status_code}"
    print("log_in_wrong_password: OK")

def log_in(email: str, password: str) -> str:
    """Test login with correct credentials"""
    k = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert k.status_code == 200, f"Unexpected status {k.status_code}"
    session_id = k.cookies.get("session_id")
    assert session_id is not None, "No session_id cookie found"
    assert k.json() == {"email": email, "message": "logged in"}
    print("log_in: OK")
    return session_id

def profile_unlogged() -> None:
    """Test accessing profile while not logged in"""
    k = requests.get(f"{BASE_URL}/profile")
    assert k.status_code == 403, f"Expected 403, got {r.status_code}"
    print("Profile_unlogged: OK")

def profile_logged(session_id: str) -> None:
    """Test accessing profile while logged in"""
    cookies = {"session_id": session_id}
    k = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert k.status_code == 200, f"Unexpected status {k.status_code}"
    assert "email" in k.json()
    print("profile_logged: OK")

def log_out(session_id: str) -> None:
    """Test logging out"""
    cookies = {"session_id": session_id}
    r = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert r.status_code == 200 or r.status_code == 302
    print("log_out: OK")

def reset_password_token(email: str) -> str:
    """Test requesting a password reset token"""
    r = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert r.status_code == 200, f"Unexpected status {r.status_code}"
    payload = r.json()
    assert payload.get("email") == email
    assert "reset_token" in payload
    print("reset_password_token: OK")
    return payload["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating the password using reset token"""
    r = requests.put(f"{BASE_URL}/reset_password",
                     data={"email": email, "reset_token": reset_token,
                           "new_password": new_password})
    assert r.status_code == 200, f"Unexpected status {r.status_code}"
    assert r.json() == {"email": email, "message": "Password updated"}
    print("update_password: OK")

if __name__ == '__main__':
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
