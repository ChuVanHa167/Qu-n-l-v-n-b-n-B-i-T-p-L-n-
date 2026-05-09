# =========================================================
# FILE: app/utils/role_required.py
# =========================================================

from functools import wraps

from flask import session
from flask import redirect
from flask import flash


# =========================================================
# ROLE REQUIRED DECORATOR
# =========================================================
def role_required(required_role):

    """
    =====================================================
    ROLE AUTHORIZATION
    =====================================================
    Ví dụ:
    @role_required("admin")
    """

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            # =============================================
            # NOT LOGIN
            # =============================================
            if "user_id" not in session:

                flash(
                    "Vui lòng đăng nhập!",
                    "error"
                )

                return redirect("/")

            # =============================================
            # WRONG ROLE
            # =============================================
            if session.get("role") != required_role:

                flash(
                    "Bạn không có quyền truy cập!",
                    "error"
                )

                return redirect("/")

            return function(*args, **kwargs)

        return wrapper

    return decorator