# =========================================================
# FILE: app/controllers/staff_controller.py
# =========================================================
# MỤC ĐÍCH:
# - Xử lý dashboard STAFF
#
# STAFF:
# - Xem văn bản được giao
# - Xử lý văn bản
# - Cập nhật trạng thái
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect

from app.models.document_model import DocumentModel


staff_bp = Blueprint(
    'staff',
    __name__
)


# =========================================================
# CHECK STAFF
# =========================================================
def check_staff():

    if 'user_id' not in session:
        return False

    if session.get('role') != 'staff':
        return False

    return True


# =========================================================
# STAFF DASHBOARD
# =========================================================
@staff_bp.route('/staff')
def staff_dashboard():

    if not check_staff():
        return redirect('/')

    documents = DocumentModel.get_all_documents()

    return render_template(
        'staff/dashboard.html',
        documents=documents
    )

# =========================================================
# ASSIGNED DOCUMENTS
# =========================================================
@staff_bp.route('/staff/assigned-documents')
def assigned_documents():

    if not check_staff():
        return redirect('/')

    documents = DocumentModel.get_all_documents()

    return render_template(
        'staff/assigned_documents.html',
        documents=documents
    )


# =========================================================
# PROCESSING DOCUMENTS
# =========================================================
@staff_bp.route('/staff/processing-documents')
def processing_documents():

    if not check_staff():
        return redirect('/')

    documents = DocumentModel.get_all_documents()

    return render_template(
        'staff/processing_documents.html',
        documents=documents
    )