# =========================================================
# FILE: app/utils/formatters.py
# =========================================================

from datetime import datetime


# =========================================================
# FORMAT DATETIME
# =========================================================
def format_datetime(date_value):

    """
    Format:
    2026-01-01 10:20:30
    =>
    01/01/2026 10:20
    """

    if not date_value:
        return ""

    try:

        dt = datetime.strptime(
            str(date_value),
            "%Y-%m-%d %H:%M:%S"
        )

        return dt.strftime("%d/%m/%Y %H:%M")

    except Exception:

        return str(date_value)


# =========================================================
# FORMAT DATE
# =========================================================
def format_date(date_value):

    if not date_value:
        return ""

    try:

        dt = datetime.strptime(
            str(date_value),
            "%Y-%m-%d %H:%M:%S"
        )

        return dt.strftime("%d/%m/%Y")

    except Exception:

        return str(date_value)


# =========================================================
# FORMAT ROLE
# =========================================================
def format_role(role):

    role_map = {

        "admin": "Quản trị viên",

        "staff": "Văn thư",

        "employee": "Nhân viên"
    }

    return role_map.get(role, role)


# =========================================================
# FORMAT STATUS
# =========================================================
def format_status(status):

    status_map = {

        "pending": "Chờ xử lý",

        "processing": "Đang xử lý",

        "approved": "Đã duyệt",

        "rejected": "Từ chối",

        "completed": "Hoàn thành"
    }

    return status_map.get(status, status)


# =========================================================
# FORMAT PRIORITY
# =========================================================
def format_priority(priority):

    priority_map = {

        "low": "Thấp",

        "normal": "Bình thường",

        "high": "Cao",

        "urgent": "Khẩn cấp"
    }

    return priority_map.get(priority, priority)


# =========================================================
# FORMAT FILE SIZE
# =========================================================
def format_file_size(size):

    """
    Byte -> KB / MB
    """

    if not size:
        return "0 KB"

    size = float(size)

    if size < 1024:
        return f"{size:.0f} B"

    if size < (1024 * 1024):
        return f"{size / 1024:.2f} KB"

    return f"{size / (1024 * 1024):.2f} MB"