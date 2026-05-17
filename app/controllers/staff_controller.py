# =========================================================
# FILE: app/controllers/staff_controller.py
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from flask import flash

from app.models.document_model import DocumentModel
from app.models.audit_log_model import AuditLogModel
from app.models.notification_model import NotificationModel


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
# DASHBOARD
# =========================================================
@staff_bp.route('/staff')
def staff_dashboard():

    if not check_staff():
        return redirect('/')

    assigned_documents = (
        DocumentModel.get_documents_by_assignee(
            session['user_id']
        )
    )

    processing_documents = (
        DocumentModel.get_staff_processing_documents(
            session['user_id']
        )
    )

    approved_documents = (
        DocumentModel.get_staff_approved_documents(
            session['user_id']
        )
    )

    pending_documents = (
        DocumentModel.get_staff_pending_documents(
            session['user_id']
        )
    )

    recent_documents = assigned_documents[:5]

    notifications = (
        NotificationModel.get_user_notifications(
            session['user_id']
        )
    )

    return render_template(
        'staff/dashboard.html',

        assigned_documents=len(assigned_documents),

        processing_documents=len(processing_documents),

        completed_documents=len(approved_documents),

        overdue_documents=len(pending_documents),

        recent_documents=recent_documents,

        notifications=notifications
    )


# =========================================================
# ASSIGNED DOCUMENTS
# =========================================================
@staff_bp.route('/staff/assigned-documents')
def assigned_documents():

    if not check_staff():
        return redirect('/')

    documents = (
        DocumentModel.get_documents_by_assignee(
            session['user_id']
        )
    )

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

    documents = (
        DocumentModel.get_staff_processing_documents(
            session['user_id']
        )
    )

    return render_template(
        'staff/processing_documents.html',
        documents=documents
    )


# =========================================================
# APPROVED DOCUMENTS
# =========================================================
@staff_bp.route('/staff/approved-documents')
def approved_documents():

    if not check_staff():
        return redirect('/')

    documents = (
        DocumentModel.get_staff_approved_documents(
            session['user_id']
        )
    )

    return render_template(
        'staff/approved_documents.html',
        documents=documents
    )


# =========================================================
# NOTIFICATIONS
# =========================================================
@staff_bp.route('/staff/notifications')
def notifications():

    if not check_staff():
        return redirect('/')

    notifications = (
        NotificationModel.get_user_notifications(
            session['user_id']
        )
    )

    unread_count = (
        NotificationModel.count_unread(
            session['user_id']
        )
    )

    return render_template(
        'staff/notifications.html',
        notifications=notifications,
        unread_count=unread_count
    )

# =========================================================
# MARK NOTIFICATION AS READ
# =========================================================
@staff_bp.route(
    '/staff/read-notification/<int:notification_id>'
)
def read_notification(notification_id):

    if not check_staff():
        return redirect('/')

    NotificationModel.mark_as_read(
        notification_id
    )

    return redirect(
        '/staff/notifications'
    )

# =========================================================
# VIEW DETAIL
# =========================================================
@staff_bp.route('/staff/document/<int:document_id>')
def staff_document_detail(document_id):

    if not check_staff():
        return redirect('/')

    document = (
        DocumentModel.get_document_full_detail(
            document_id
        )
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
        'staff/workflow_detail.html',

        document=document,

        comments=comments,

        history=history
    )


# =========================================================
# TAKE DOCUMENT
# =========================================================
@staff_bp.route(
    '/staff/take-document/<int:document_id>',
    methods=['POST']
)
def take_document(document_id):

    if not check_staff():
        return redirect('/')

    DocumentModel.staff_take_document(
        document_id,
        session['user_id']
    )

    AuditLogModel.create_log(
        session['user_id'],
        'TAKE_DOCUMENT',
        'DOCUMENT',
        document_id,
        f"{session['username']} nhận xử lý văn bản"
    )

    NotificationModel.create_notification(
        session['user_id'],
        'Đã nhận văn bản',
        f'Bạn đã nhận xử lý văn bản #{document_id}'
    )

    flash('Đã nhận xử lý văn bản')

    return redirect(
        '/staff/processing-documents'
    )


# =========================================================
# COMPLETE DOCUMENT
# =========================================================
@staff_bp.route(
    '/staff/complete-document/<int:document_id>',
    methods=['POST']
)
def complete_document(document_id):

    if not check_staff():
        return redirect('/')

    DocumentModel.staff_complete_document(
        document_id
    )

    DocumentModel.create_approval_history(
        document_id,
        'APPROVED',
        'Staff hoàn thành xử lý',
        session['user_id']
    )

    AuditLogModel.create_log(
        session['user_id'],
        'COMPLETE_DOCUMENT',
        'DOCUMENT',
        document_id,
        f"{session['username']} hoàn thành văn bản"
    )

    NotificationModel.create_notification(
        session['user_id'],
        'Hoàn thành văn bản',
        f'Văn bản #{document_id} đã hoàn thành'
    )

    flash('Đã hoàn thành văn bản')

    return redirect(
        '/staff/approved-documents'
    )


# =========================================================
# COMMENT DOCUMENT
# =========================================================
@staff_bp.route(
    '/staff/comment/<int:document_id>',
    methods=['POST']
)
def add_comment(document_id):

    if not check_staff():
        return redirect('/')

    comment = request.form.get(
        'comment'
    )

    DocumentModel.add_comment(
        document_id,
        session['user_id'],
        comment
    )

    flash('Đã thêm bình luận')

    return redirect(
        f'/staff/document/{document_id}'
    )

# =========================================================
# UPDATE DOCUMENT STATUS
# =========================================================
@staff_bp.route(
    '/staff/update-status/<int:document_id>',
    methods=['POST']
)
def update_document_status(document_id):

    if not check_staff():
        return redirect('/')

    new_status = request.form.get(
        'status'
    )

    document = (
        DocumentModel.get_document_by_id(
            document_id
        )
    )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    DocumentModel.update_document_status(
        document_id,
        new_status
    )

    # =====================================================
    # CREATE APPROVAL HISTORY
    # =====================================================

    DocumentModel.create_approval_history(
        document_id,
        new_status.upper(),
        f"Staff cập nhật trạng thái -> {new_status}",
        session['user_id']
    )

    # =====================================================
    # CREATE NOTIFICATION
    # =====================================================

    if document['created_by']:

        NotificationModel.create_notification(
            document['created_by'],
            'Cập nhật văn bản',
            f"Văn bản '{document['title']}' đã chuyển sang trạng thái '{new_status}'"
        )

    # =====================================================
    # AUDIT LOG
    # =====================================================

    AuditLogModel.create_log(
        session['user_id'],
        'UPDATE_DOCUMENT_STATUS',
        'DOCUMENT',
        document_id,
        f"{session['username']} cập nhật trạng thái văn bản thành {new_status}"
    )

    flash('Cập nhật trạng thái thành công')

    if new_status == 'approved':

        return redirect(
            '/staff/approved-documents'
        )

    return redirect(
        '/staff/processing-documents'
    )