#!/usr/bin/env python3
"""
Main file
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Test user's registration API
    """
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    response_status_code = response.status_code
    if response_status_code == 200:
        expected_response = {
            'email': 'guillaume@holberton.io',
            'message': 'user created'}
    else:
        expected_response = {'message': 'email already registered'}
    response = response.json()
    assert response == expected_response


def log_in_wrong_password(email: str, password: str) -> None:
    """Test user login API with a wrong password
    """
    url = "http://localhost:5000/sessions"
    wrong_credentials = {"email": email, "password": password}
    response = requests.post(url, data=wrong_credentials)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test user login API with correct credentials
    """
    url = "http://localhost:5000/sessions"
    valid_credentials = {"email": email, "password": password}
    response = requests.post(url, data=valid_credentials)
    session_id = response.cookies.get("session_id")
    assert response.status_code == 200
    return session_id


def profile_unlogged() -> None:
    """Test user's profile API with unlogged user
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 200


def profile_logged(session_id: str) -> None:
    """Test user's profile API with logged user
    """
    url = "http://localhost:5000/profile"
    cookie = {"session_id": session_id}
    response = requests.get(url, cookies=cookie).json()
    expected_response = {'email': 'guillaume@holberton.io'}
    assert response == expected_response


def log_out(session_id: str) -> None:
    """Test user logout API
    """
    url = "http://localhost:5000/sessions"
    cookie = {"session_id": session_id}
    response = requests.delete(url, cookies=cookie).json()
    expected_response = {'message': 'Bienvenue'}
    assert response == expected_response


def reset_password_token(email: str) -> str:
    """Test user reset password token API
    """
    url = "http://localhost:5000/reset_password"
    email = {"email": email}
    response = requests.post(url, data=email).json()
    reset_token = response.get("reset_token")
    expected_response = {
        'email': 'guillaume@holberton.io',
        'reset_token': reset_token}
    assert response == expected_response
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test user's password update API
    """
    url = "http://localhost:5000/reset_password"
    email = {
        "email": EMAIL,
        "reset_token": reset_token,
        "new_password": new_password}
    response = requests.put(url, data=email).json()
    expected_output = {
        'email': 'guillaume@holberton.io',
        'message': 'Password updated'}
    assert response == expected_output


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
