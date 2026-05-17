# =========================================================
# FILE: app/controllers/employee_controller.py
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from flask import flash

from app.models.document_model import DocumentModel
from app.models.notification_model import NotificationModel
from app.models.audit_log_model import AuditLogModel


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

    if session.get('role') != 'employee':
        return False

    return True


# =========================================================
# DASHBOARD
# =========================================================
@employee_bp.route('/employee')
def employee_dashboard():

    if not check_employee():
        return redirect('/')

    my_documents = (
        DocumentModel.get_documents_by_creator(
            session['user_id']
        )
    )

    pending_count = 0
    processing_count = 0
    approved_count = 0
    rejected_count = 0

    for doc in my_documents:

        if doc['status'] == 'pending':
            pending_count += 1

        elif doc['status'] == 'processing':
            processing_count += 1

        elif doc['status'] == 'approved':
            approved_count += 1

        elif doc['status'] == 'rejected':
            rejected_count += 1

    recent_documents = my_documents[:5]

    return render_template(
        'employee/dashboard.html',

        pending_count=pending_count,

        processing_count=processing_count,

        approved_count=approved_count,

        rejected_count=rejected_count,

        recent_documents=recent_documents
    )


# =========================================================
# MY DOCUMENTS
# =========================================================
@employee_bp.route('/employee/my-documents')
def my_documents():

    if not check_employee():
        return redirect('/')

    documents = (
        DocumentModel.get_documents_by_creator(
            session['user_id']
        )
    )

    return render_template(
        'employee/my_documents.html',
        documents=documents
    )


# =========================================================
# DOCUMENT DETAIL
# =========================================================
@employee_bp.route('/employee/document/<int:document_id>')
def employee_document_detail(document_id):

    if not check_employee():
        return redirect('/')

    document = (
        DocumentModel.get_document_full_detail(
            document_id
        )
    )

    if not document:

        flash('Không tìm thấy văn bản')

        return redirect(
            '/employee/my-documents'
        )

    comments = (
        DocumentModel.get_document_comments(
            document_id
        )
    )

    history = (
        DocumentModel.get_approval_history(
            document_id
        )
    )

    return render_template(
        'employee/document_detail.html',

        document=document,

        comments=comments,

        history=history
    )


# =========================================================
# ADD COMMENT
# =========================================================
@employee_bp.route(
    '/employee/document/comment/<int:document_id>',
    methods=['POST']
)
def employee_add_comment(document_id):

    if not check_employee():
        return redirect('/')

    comment = request.form.get(
        'comment'
    )

    if comment:

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
            'Employee thêm bình luận'
        )

    flash('Đã thêm bình luận')

    return redirect(
        f'/employee/document/{document_id}'
    )


# =========================================================
# NOTIFICATIONS
# =========================================================
@employee_bp.route('/employee/notifications')
def employee_notifications():

    if not check_employee():
        return redirect('/')

    notifications = (
        NotificationModel.get_user_notifications(
            session['user_id']
        )
    )

    return render_template(
        'employee/notifications.html',
        notifications=notifications
    )