#!/usr/bin/env python
"""
Main test module for the authentication service
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test registering a new user"""
    r = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert r.status_code == 200, f"Unexpected status {r.status_code}"
    assert r.json() == {"email": email, "message": "user created"}
    print("register_user: OK")


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password"""
    r = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert r.status_code == 401, f"Expected 401, got {r.status_code}"
    print("log_in_wrong_password: OK")


def log_in(email: str, password: str) -> str:
    """Test login with correct credentials"""
    r = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert r.status_code == 200, f"Unexpected status {r.status_code}"
    session_id = r.cookies.get("session_id")
    assert session_id is not None, "No session_id cookie found"
    assert r.json() == {"email": email, "message": "logged in"}
    print("log_in: OK")
    return session_id


def profile_unlogged() -> None:
    """Test accessing profile while not logged in"""
    r = requests.get(f"{BASE_URL}/profile")
    assert r.status_code == 403, f"Expected 403, got {r.status_code}"
    print("profile_unlogged: OK")


def profile_logged(session_id: str) -> None:
    """Test accessing profile while logged in"""
    cookies = {"session_id": session_id}
    r = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert r.status_code == 200, f"Unexpected status {r.status_code}"
    assert "email" in r.json()
    print("profile_logged: OK")


def log_out(session_id: str) -> None:
    """Test logging out"""
    cookies = {"session_id": session_id}
    r = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    # Expecting a redirect to `/`
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


# ========== RUN TESTS ==========
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

