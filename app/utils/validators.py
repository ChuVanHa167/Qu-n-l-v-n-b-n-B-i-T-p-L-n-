import re


# =========================
# USERNAME VALIDATION
# =========================
def validate_username(username):

    if not username:
        return False, "Username không được để trống"

    if len(username) < 3:
        return False, "Username phải >= 3 ký tự"

    return True, ""


# =========================
# PASSWORD VALIDATION
# =========================
def validate_password(password):

    if not password:
        return False, "Password không được để trống"

    if len(password) < 6:
        return False, "Password phải >= 6 ký tự"

    return True, ""


# =========================
# EMAIL VALIDATION
# =========================
def validate_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(pattern, email):
        return False, "Email không hợp lệ"

    return True, ""


# =========================
# DOCUMENT VALIDATION
# =========================
def validate_document(title, content):

    if not title:
        return False, "Tiêu đề không được để trống"

    if len(title) < 5:
        return False, "Tiêu đề quá ngắn"

    if not content:
        return False, "Nội dung không được để trống"

    return True, ""