# =========================================================
# FILE: app/routes.py
# =========================================================

"""
=========================================================
ROUTES MANAGER
=========================================================

MỤC ĐÍCH:
- Quản lý tập trung toàn bộ Blueprint
- Dễ mở rộng hệ thống
- Tránh import rời rạc trong app.py

LỢI ÍCH:
- Scale lớn dễ quản lý
- Có thể tách module sau này
=========================================================
"""

# =========================================================
# IMPORT BLUEPRINTS
# =========================================================
from app.controllers.auth_controller import auth_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.staff_controller import staff_bp
from app.controllers.employee_controller import employee_bp
from app.controllers.document_controller import document_bp


# =========================================================
# ALL BLUEPRINTS
# =========================================================
ALL_BLUEPRINTS = [

    # AUTH
    auth_bp,

    # ADMIN
    admin_bp,

    # STAFF
    staff_bp,

    # EMPLOYEE
    employee_bp,

    # DOCUMENT
    document_bp
]