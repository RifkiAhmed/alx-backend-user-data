#!/usr/bin/env python3
# """
# Route module for the API
# """
# from flask import Flask, abort, jsonify, redirect, request
# from auth import Auth

# app = Flask(__name__)
# AUTH = Auth()


# @app.route("/", methods=["GET"])
# def index() -> str:
#     """Index page
#     """
#     return jsonify({"message": "Bienvenue"})


# @app.route("/users", methods=["POST"])
# def users() -> str:
#     """User registration
#     """
#     try:
#         email = request.form.get("email")
#         password = request.form.get("password")
#         AUTH.register_user(email, password)
#         return jsonify({"email": email, "message": "user created"})
#     except ValueError:
#         return jsonify({"message": "email already registered"}), 400


# @app.route("/sessions", methods=["POST"])
# def login() -> str:
#     """User login
#     """
#     email = request.form.get("email")
#     password = request.form.get("password")
#     _valid_lagin = AUTH.valid_login(email, password)
#     if not _valid_lagin:
#         abort(401)
#     session_id = AUTH.create_session(email)
#     response = jsonify({"email": email, "message": "logged in"})
#     response.set_cookie("session_id", session_id)
#     return response


# # @app.route("/sessions", methods=["DELETE"])
# # def logout() -> None:
# #     """User logout
# #     """
# #     user = None
# #     session_id = request.cookies.get("session_id")
# #     if session_id:
# #         user = AUTH.get_user_from_session_id(session_id)
# #     if not user:
# #         abort(403)
# #     AUTH.destroy_session(user.id)
# #     return redirect("/")


# @app.route("/sessions", methods=["DELETE"], strict_slashes=False)
# def logout() -> None:
#     """Handle a DELETE request to log out a user."""
#     user = None
#     session_id = request.cookies.get("session_id")
#     if session_id:
#         user = AUTH.get_user_from_session_id(session_id)
#     if not user:
#         abort(403)
#     AUTH.destroy_session(user.id)
#     return redirect('/')


# @app.route("/profile", methods=["GET"])
# def profile():  # -> str:
#     """User profile
#     """
#     user = None
#     session_id = request.cookies.get("session_id")
#     if session_id:
#         user = AUTH.get_user_from_session_id(session_id)
#     if not user:
#         abort(403)
#     return jsonify({"email": user.email}), 200


# @app.route("/reset_password", methods=["POST"])
# def get_reset_password_token() -> str:
#     """User reset password token
#     """
#     email = request.form.get("email")
#     try:
#         token = AUTH.get_reset_password_token(email)
#         return jsonify({"email": email, "reset_token": token}), 200
#     except ValueError:
#         abort(403)


# @app.route("/reset_password", methods=["PUT"])
# def update_password() -> str:
#     """User password update
#     """
#     email = request.form.get("email")
#     reset_token = request.form.get("reset_token")
#     new_password = request.form.get("new_password")
#     try:
#         AUTH.update_password(reset_token, new_password)
#         return jsonify({"email": email, "message": "Password updated"}), 200
#     except ValueError:
#         abort(403)


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port="5000")
"""Flask app module"""
from flask import Flask, request, jsonify, make_response, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """GET route to return a JSON payload."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """Endpoint to register a user."""
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Endpoint to handle user login."""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)

        response_data = {"email": email, "message": "logged in"}
        response = make_response(jsonify(response_data), 200)
        response.set_cookie("session_id", session_id)

        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> None:
    """Handle a DELETE request to log out a user."""
    user = None
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Look out the user in database and return 200 code if ok"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route(
        "/reset_password",
        methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Extract email from form data"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    response = {"email": email, "reset_token": reset_token}
    return jsonify(response), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def reset_password():
    """Update password end-point"""
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    reset_token = request.form.get('reset_token')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    response = {"email": email, "message": "Password updated"}
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
