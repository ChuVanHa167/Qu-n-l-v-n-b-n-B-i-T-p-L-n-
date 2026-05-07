"""
File này dùng để import tất cả route/controller.
Sau này nếu dự án lớn có thể quản lý route tập trung tại đây.
"""

from app.controllers.auth_controller import auth_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.staff_controller import staff_bp
from app.controllers.employee_controller import employee_bp
from app.controllers.document_controller import document_bp


ALL_BLUEPRINTS = [
    auth_bp,
    admin_bp,
    staff_bp,
    employee_bp,
    document_bp
]