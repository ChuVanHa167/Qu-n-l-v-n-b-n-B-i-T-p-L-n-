# =========================================================
# FILE: app/controllers/employee_controller.py
# =========================================================
# MỤC ĐÍCH:
# - Dashboard nhân viên thường
#
# EMPLOYEE:
# - Xem văn bản cá nhân
# - Theo dõi trạng thái
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect

from app.models.document_model import DocumentModel


employee_bp = Blueprint(
    'employee',
    __name__
)


# =========================================================
# CHECK EMPLOYEE
# =========================================================
def check_employee():

    if 'user_id' not in session:
        return False

    return session.get('role') == 'employee'


# =========================================================
# EMPLOYEE DASHBOARD
# =========================================================
@employee_bp.route('/employee')
def employee_dashboard():

    if not check_employee():
        return redirect('/')

    documents = DocumentModel.get_all_documents()

    return render_template(
        'employee/dashboard.html',
        documents=documents
    )

# =========================================================
# MY DOCUMENTS
# =========================================================
@employee_bp.route('/employee/my-documents')
def my_documents():

    if not check_employee():
        return redirect('/')

    documents = DocumentModel.get_all_documents()

    return render_template(
        'employee/my_documents.html',
        documents=documents
    )