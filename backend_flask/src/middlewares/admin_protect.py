# These acts like middleware, defining rules that needs to be followed before accessing a route
# For example, there could be certain routes that only authenticated users can access, so we can
# define a middleware that checks if the user is authenticated or not and stuffs like that
from flask import request, jsonify, g
from functools import wraps


def protect_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the token from the Authorization header
        user = g.user
        if not user.is_admin:
            raise ValueError("You don't have permission")
        return f(*args, **kwargs)

    return decorated_function
