# =========================================================
# FILE: app/controllers/admin_controller.py
# =========================================================
# MỤC ĐÍCH:
# - Xử lý toàn bộ chức năng ADMIN
#
# ADMIN:
# - Dashboard
# - User management
# - Document management
# - Audit logs
# - Settings
#
# SOLID:
# - Admin controller chỉ xử lý admin
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from app.models.user_model import UserModel
from app.models.document_model import DocumentModel
from app.models.audit_log_model import AuditLogModel


admin_bp = Blueprint(
    'admin',
    __name__
)


# =========================================================
# CHECK ADMIN
# =========================================================
def check_admin():

    if 'user_id' not in session:
        return False

    if session.get('role') != 'admin':
        return False

    return True


# =========================================================
# ADMIN DASHBOARD
# =========================================================
@admin_bp.route('/admin')
@admin_bp.route('/admin/index')
def dashboard():

    if not check_admin():
        return redirect('/')

    total_users = UserModel.count_users()

    total_documents = DocumentModel.count_documents()

    pending_documents = DocumentModel.count_by_status(
        'pending'
    )

    completed_documents = DocumentModel.count_by_status(
        'completed'
    )

    return render_template(
        'admin/dashboard.html',

        total_users=total_users,
        total_documents=total_documents,
        pending_documents=pending_documents,
        completed_documents=completed_documents
    )


# =========================================================
# USERS PAGE
# =========================================================
@admin_bp.route('/admin/users')
def users_page():

    if not check_admin():
        return redirect('/')

    users = UserModel.get_all_users()

    return render_template(
        'admin/users.html',
        users=users
    )


# =========================================================
# CREATE USER
# =========================================================
@admin_bp.route('/admin/users/create', methods=['POST'])
def create_user():

    if not check_admin():
        return redirect('/')

    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    UserModel.create_user(
        username,
        password,
        role
    )

    AuditLogModel.create_log(
        session['user_id'],
        'CREATE_USER',
        'USER',
        None,
        f"Admin tạo user {username}"
    )

    return redirect('/admin/users')


# =========================================================
# DELETE USER
# =========================================================
@admin_bp.route('/admin/users/delete/<int:user_id>')
def delete_user(user_id):

    if not check_admin():
        return redirect('/')

    UserModel.delete_user(user_id)

    AuditLogModel.create_log(
        session['user_id'],
        'DELETE_USER',
        'USER',
        user_id,
        'Admin xóa user'
    )

    return redirect('/admin/users')


# =========================================================
# DOCUMENT PAGE
# =========================================================
@admin_bp.route('/admin/documents')
def documents_page():

    if not check_admin():
        return redirect('/')

    documents = DocumentModel.get_all_documents()

    return render_template(
        'admin/documents.html',
        documents=documents
    )


# =========================================================
# CREATE DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/create',
    methods=['POST']
)
def create_document():

    if not check_admin():
        return redirect('/')

    title = request.form.get('title')
    content = request.form.get('content')
    document_type = request.form.get('document_type')

    DocumentModel.create_document(
        title,
        content,
        document_type,
        session['user_id']
    )

    AuditLogModel.create_log(
        session['user_id'],
        'CREATE_DOCUMENT',
        'DOCUMENT',
        None,
        f"Tạo văn bản {title}"
    )

    return redirect('/admin/documents')


# =========================================================
# DELETE DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/delete/<int:document_id>'
)
def delete_document(document_id):

    if not check_admin():
        return redirect('/')

    DocumentModel.delete_document(document_id)

    AuditLogModel.create_log(
        session['user_id'],
        'DELETE_DOCUMENT',
        'DOCUMENT',
        document_id,
        'Xóa văn bản'
    )

    return redirect('/admin/documents')


# =========================================================
# AUDIT PAGE
# =========================================================
@admin_bp.route('/admin/audit')
def audit_page():

    if not check_admin():
        return redirect('/')

    logs = AuditLogModel.get_all_logs()

    return render_template(
        'admin/audit_logs.html',
        logs=logs
    )


# =========================================================
# SETTINGS PAGE
# =========================================================
@admin_bp.route('/admin/settings')
def settings_page():

    if not check_admin():
        return redirect('/')

    return render_template(
        'admin/settings.html'
    )