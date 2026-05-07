from functools import wraps
from flask import session, redirect


# =========================
# ROLE REQUIRED DECORATOR
# =========================
def role_required(required_role):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            # chưa login
            if "role" not in session:
                return redirect("/")

            # sai role
            if session.get("role") != required_role:
                return redirect("/")

            return function(*args, **kwargs)

        return wrapper

    return decorator