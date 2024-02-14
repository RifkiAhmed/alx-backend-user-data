#!/usr/bin/env python3
""" Module of SessionAuth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    User login
    """
    user_email = request.form.get("email")
    user_pwd = request.form.get("password")
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400
    users = User.search(attributes={"email": user_email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    current_user = None
    for user in users:
        if user.is_valid_password(pwd=user_pwd):
            current_user = user
            break
    if not current_user:
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        auth = SessionAuth()
        session_id = auth.create_session(current_user.id)
        response = jsonify(current_user.to_json())
        session_name = os.getenv("SESSION_NAME")
        response.set_cookie(session_name, session_id)
        return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ POST /api/v1/auth_session/login
    User login
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
