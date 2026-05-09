# =========================================================
# FILE: app/controllers/document_controller.py
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash

from app.models.document_model import DocumentModel
from app.models.audit_log_model import AuditLogModel
from app.models.user_model import UserModel


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

    comments = DocumentModel.get_document_comments(
        document_id
    )

    return render_template(
        'documents/detail.html',
        document=document,
        comments=comments
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

    note = request.form.get('note')

    DocumentModel.update_document_status(
        document_id,
        status
    )

    # lưu lịch sử phê duyệt
    DocumentModel.create_approval_history(
        document_id=document_id,
        action=status,
        note=note,
        processed_by=session['user_id']
    )

    AuditLogModel.create_log(
        session['user_id'],
        'UPDATE_DOCUMENT_STATUS',
        'DOCUMENT',
        document_id,
        f"Cập nhật trạng thái thành {status}"
    )

    flash('Cập nhật trạng thái thành công')

    # redirect theo role
    role = session.get('role')

    if role == 'admin':
        return redirect('/admin/documents')

    elif role == 'staff':
        return redirect('/staff/processing-documents')

    else:
        return redirect('/employee/my-documents')


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

    assigned_to = request.form.get(
        'assigned_to'
    )

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

    flash('Phân công thành công')

    return redirect('/admin/documents')


# =========================================================
# APPROVE DOCUMENT
# =========================================================
@document_bp.route(
    '/documents/approve/<int:document_id>'
)
def approve_document(document_id):

    if not check_login():
        return redirect('/')

    DocumentModel.update_document_status(
        document_id,
        'approved'
    )

    AuditLogModel.create_log(
        session['user_id'],
        'APPROVE_DOCUMENT',
        'DOCUMENT',
        document_id,
        'Duyệt văn bản'
    )

    flash('Đã duyệt văn bản')

    return redirect('/staff/processing-documents')


# =========================================================
# REJECT DOCUMENT
# =========================================================
@document_bp.route(
    '/documents/reject/<int:document_id>',
    methods=['POST']
)
def reject_document(document_id):

    if not check_login():
        return redirect('/')

    reason = request.form.get('reason')

    DocumentModel.reject_document(
        document_id,
        reason
    )

    AuditLogModel.create_log(
        session['user_id'],
        'REJECT_DOCUMENT',
        'DOCUMENT',
        document_id,
        'Từ chối văn bản'
    )

    flash('Đã từ chối văn bản')

    return redirect('/staff/processing-documents')


# =========================================================
# ADD COMMENT
# =========================================================
@document_bp.route(
    '/documents/comment/<int:document_id>',
    methods=['POST']
)
def add_comment(document_id):

    if not check_login():
        return redirect('/')

    comment = request.form.get(
        'comment'
    )

    DocumentModel.add_comment(
        document_id,
        session['user_id'],
        comment
    )

    AuditLogModel.create_log(
        session['user_id'],
        'COMMENT_DOCUMENT',
        'DOCUMENT',
        document_id,
        'Bình luận văn bản'
    )

    flash('Đã thêm bình luận')

    return redirect(
        f'/documents/{document_id}'
    )