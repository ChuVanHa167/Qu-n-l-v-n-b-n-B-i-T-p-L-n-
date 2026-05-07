from functools import wraps
from flask import session, redirect


# =========================
# LOGIN REQUIRED DECORATOR
# =========================
def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        # chưa login
        if "user_id" not in session:
            return redirect("/")

        return function(*args, **kwargs)

    return wrapper