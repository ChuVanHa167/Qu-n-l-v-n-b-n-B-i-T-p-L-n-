# =========================================================
# FILE: app/utils/login_required.py
# =========================================================

from functools import wraps

from flask import session
from flask import redirect
from flask import flash


# =========================================================
# LOGIN REQUIRED DECORATOR
# =========================================================
def login_required(function):

    """
    =====================================================
    CHECK USER LOGIN
    =====================================================
    Nếu chưa login:
    -> redirect login page
    """

    @wraps(function)
    def wrapper(*args, **kwargs):

        # =================================================
        # USER NOT LOGIN
        # =================================================
        if "user_id" not in session:

            flash(
                "Vui lòng đăng nhập để tiếp tục!",
                "error"
            )

            return redirect("/")

        return function(*args, **kwargs)

    return wrapper