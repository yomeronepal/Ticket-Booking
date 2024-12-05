# These acts like middleware, defining rules that needs to be followed before accessing a route
# For example, there could be certain routes that only authenticated users can access, so we can
# define a middleware that checks if the user is authenticated or not and stuffs like that
from flask import request, jsonify, g
from functools import wraps

from ..database.models import User
from ..utils.token import get_token
import jwt
import os


def protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return (
                jsonify(
                    {"message": "Unauthorized! You need to provide a Bearer token"}
                ),
                401,
            )

        # Extract the token
        token = auth_header.split(" ")[1]

        # Decode and validate the token
        try:
            decoded = jwt.decode(
                token,
                os.getenv("JWT_SECRET", "your_default_secret_key"),
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired! Please login again"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token. Please log in again."}), 401

        # Extract the user ID or other relevant data from the token
        user_id = decoded.get("id")
        if not user_id:
            return jsonify({"error": "Login is required to access this!"}), 401

        # Find the user in the database
        # Replace the following with your actual database logic
        user = User.query.filter_by(
            id=user_id
        ).first()  # Example: User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found. Please log in again!"}), 401

        # Attach the user to Flask's `g` context for use in the route
        g.user = user

        # Proceed to the decorated route
        return f(*args, **kwargs)

    return decorated_function
