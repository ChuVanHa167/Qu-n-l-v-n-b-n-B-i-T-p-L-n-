# =========================================================
# FILE: app/utils/validators.py
# =========================================================

import re


# =========================================================
# VALIDATE USERNAME
# =========================================================
def validate_username(username):

    if not username:
        return False, "Username không được để trống"

    username = username.strip()

    if len(username) < 3:
        return False, "Username phải >= 3 ký tự"

    if len(username) > 50:
        return False, "Username quá dài"

    pattern = r'^[a-zA-Z0-9_]+$'

    if not re.match(pattern, username):

        return (
            False,
            "Username chỉ được chứa chữ, số và dấu _"
        )

    return True, ""


# =========================================================
# VALIDATE PASSWORD
# =========================================================
def validate_password(password):

    if not password:
        return False, "Password không được để trống"

    if len(password) < 6:
        return False, "Password phải >= 6 ký tự"

    if len(password) > 100:
        return False, "Password quá dài"

    return True, ""


# =========================================================
# VALIDATE EMAIL
# =========================================================
def validate_email(email):

    if not email:
        return False, "Email không được để trống"

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(pattern, email):

        return False, "Email không hợp lệ"

    return True, ""


# =========================================================
# VALIDATE PHONE
# =========================================================
def validate_phone(phone):

    if not phone:
        return True, ""

    pattern = r'^[0-9]{9,11}$'

    if not re.match(pattern, phone):

        return False, "Số điện thoại không hợp lệ"

    return True, ""


# =========================================================
# VALIDATE DOCUMENT
# =========================================================
def validate_document(title, content):

    if not title:
        return False, "Tiêu đề không được để trống"

    title = title.strip()

    if len(title) < 5:
        return False, "Tiêu đề phải >= 5 ký tự"

    if len(title) > 255:
        return False, "Tiêu đề quá dài"

    if not content:
        return False, "Nội dung không được để trống"

    return True, ""


# =========================================================
# VALIDATE FILE EXTENSION
# =========================================================
def validate_file_extension(filename):

    allowed_extensions = {
        'pdf',
        'doc',
        'docx',
        'xls',
        'xlsx',
        'png',
        'jpg',
        'jpeg'
    }

    if '.' not in filename:
        return False

    extension = filename.rsplit('.', 1)[1].lower()

    return extension in allowed_extensions