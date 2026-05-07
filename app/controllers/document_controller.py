# =========================================================
# FILE: app/controllers/document_controller.py
# =========================================================
# MỤC ĐÍCH:
# - Xử lý document chung
#
# DOCUMENT:
# - View detail
# - Update status
# - Assign document
#
# SOLID:
# - Tách riêng document logic
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from app.models.document_model import DocumentModel
from app.models.audit_log_model import AuditLogModel


document_bp = Blueprint(
    'document',
    __name__
)


# =========================================================
# CHECK LOGIN
# =========================================================
def check_login():

    return 'user_id' in session


# =========================================================
# DOCUMENT DETAIL
# =========================================================
@document_bp.route('/documents/<int:document_id>')
def document_detail(document_id):

    if not check_login():
        return redirect('/')

    document = DocumentModel.get_document_by_id(
        document_id
    )

    return render_template(
        'documents/detail.html',
        document=document
    )


# =========================================================
# UPDATE STATUS
# =========================================================
@document_bp.route(
    '/documents/update-status/<int:document_id>',
    methods=['POST']
)
def update_status(document_id):

    if not check_login():
        return redirect('/')

    status = request.form.get('status')

    DocumentModel.update_document_status(
        document_id,
        status
    )

    AuditLogModel.create_log(
        session['user_id'],
        'UPDATE_DOCUMENT_STATUS',
        'DOCUMENT',
        document_id,
        f"Cập nhật trạng thái thành {status}"
    )

    return redirect('/admin/documents')


# =========================================================
# ASSIGN DOCUMENT
# =========================================================
@document_bp.route(
    '/documents/assign/<int:document_id>',
    methods=['POST']
)
def assign_document(document_id):

    if not check_login():
        return redirect('/')

    assigned_to = request.form.get('assigned_to')

    DocumentModel.assign_document(
        document_id,
        assigned_to
    )

    AuditLogModel.create_log(
        session['user_id'],
        'ASSIGN_DOCUMENT',
        'DOCUMENT',
        document_id,
        'Phân công xử lý văn bản'
    )

    return redirect('/admin/documents')