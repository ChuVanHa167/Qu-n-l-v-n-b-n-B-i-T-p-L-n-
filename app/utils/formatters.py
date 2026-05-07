from datetime import datetime


# =========================
# FORMAT DATETIME
# =========================
def format_datetime(date_value):

    if not date_value:
        return ""

    try:
        dt = datetime.strptime(
            str(date_value),
            "%Y-%m-%d %H:%M:%S"
        )

        return dt.strftime("%d/%m/%Y %H:%M")

    except:
        return str(date_value)


# =========================
# FORMAT ROLE
# =========================
def format_role(role):

    role_map = {
        "admin": "Quản trị viên",
        "staff": "Văn thư",
        "employee": "Nhân viên"
    }

    return role_map.get(role, role)


# =========================
# FORMAT STATUS
# =========================
def format_status(status):

    status_map = {
        "pending": "Chờ xử lý",
        "processing": "Đang xử lý",
        "approved": "Đã duyệt",
        "rejected": "Từ chối",
        "completed": "Hoàn thành"
    }

    return status_map.get(status, status)