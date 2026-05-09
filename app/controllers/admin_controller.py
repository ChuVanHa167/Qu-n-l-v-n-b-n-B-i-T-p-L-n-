# =========================================================
# FILE: app/controllers/admin_controller.py
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash

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

    processing_documents = DocumentModel.count_by_status(
        'processing'
    )

    approved_documents = DocumentModel.count_by_status(
        'approved'
    )

    rejected_documents = DocumentModel.count_by_status(
        'rejected'
    )

    recent_documents = DocumentModel.get_recent_documents()

    recent_logs = AuditLogModel.get_recent_logs()

    return render_template(
        'admin/dashboard.html',

        total_users=total_users,
        total_documents=total_documents,

        pending_documents=pending_documents,
        processing_documents=processing_documents,
        approved_documents=approved_documents,
        rejected_documents=rejected_documents,

        recent_documents=recent_documents,
        recent_logs=recent_logs
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
        users=users,
        edit_user=None
    )


# =========================================================
# CREATE USER
# =========================================================
@admin_bp.route(
    '/admin/users/create',
    methods=['POST']
)
def create_user():

    try:

        print("=== CREATE USER START ===")

        if not check_admin():
            print("KHONG PHAI ADMIN")
            return redirect('/')

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', '').strip()

        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        print(username)
        print(password)
        print(role)
        print(full_name)
        print(email)
        print(phone)

        if UserModel.user_exists(username):

            flash('Username đã tồn tại')

            return redirect('/admin/users')

        UserModel.create_user(
            username,
            password,
            role,
            full_name,
            email,
            phone
        )

        print("INSERT THANH CONG")

        flash('Tạo user thành công')

        return redirect('/admin/users')

    except Exception as e:

        print("LOI CREATE USER:")
        print(e)

        flash(str(e))

        return redirect('/admin/users')

# =========================================================
# UPDATE USER ROLE
# =========================================================
@admin_bp.route(
    '/admin/users/update-role/<int:user_id>',
    methods=['POST']
)
def update_user_role(user_id):

    if not check_admin():
        return redirect('/')

    role = request.form.get('role')

    UserModel.update_role(
        user_id,
        role
    )

    AuditLogModel.create_log(
        session['user_id'],
        'UPDATE_USER_ROLE',
        'USER',
        user_id,
        f"Cập nhật role thành {role}"
    )

    return redirect('/admin/users')


# =========================================================
# UPDATE USER STATUS
# =========================================================
@admin_bp.route(
    '/admin/users/update-status/<int:user_id>'
)
def update_user_status(user_id):

    if not check_admin():
        return redirect('/')

    user = UserModel.find_by_id(user_id)

    # đảo trạng thái active
    new_status = 0 if user['is_active'] == 1 else 1

    UserModel.update_status(
        user_id,
        new_status
    )

    AuditLogModel.create_log(
        session['user_id'],
        'UPDATE_USER_STATUS',
        'USER',
        user_id,
        'Cập nhật trạng thái tài khoản'
    )

    return redirect('/admin/users')


# =========================================================
# DELETE USER
# =========================================================
@admin_bp.route('/admin/users/delete/<int:user_id>')
def delete_user(user_id):

    if not check_admin():
        return redirect('/')

    # không cho admin tự xóa chính mình
    if session['user_id'] == user_id:

        flash('Không thể xóa tài khoản admin hiện tại')

        return redirect('/admin/users')

    user = UserModel.find_by_id(user_id)

    if not user:

        flash('User không tồn tại')

        return redirect('/admin/users')

    # lưu username trước khi xóa
    username = user['username']

    # xóa user
    UserModel.delete_user(user_id)

    # ghi log SAU KHI XÓA
    # nhưng dùng admin hiện tại
    AuditLogModel.create_log(
        session['user_id'],
        'DELETE_USER',
        'USER',
        user_id,
        f'Admin đã xóa user {username}'
    )

    flash('Xóa user thành công')

    return redirect('/admin/users')


# =========================================================
# DOCUMENT PAGE
# =========================================================
@admin_bp.route('/admin/documents')
def documents_page():

    if not check_admin():
        return redirect('/')

    documents = DocumentModel.get_all_documents()

    users = UserModel.get_all_users()

    return render_template(
        'admin/documents.html',
        documents=documents,
        users=users
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

    document_type = request.form.get(
        'document_type'
    )

    category = request.form.get(
        'category'
    )

    priority = request.form.get(
        'priority'
    )

    DocumentModel.create_document(
        title=title,
        content=content,
        document_type=document_type,
        category=category,
        priority=priority,
        created_by=session['user_id']
    )

    AuditLogModel.create_log(
        session['user_id'],
        'CREATE_DOCUMENT',
        'DOCUMENT',
        None,
        f"Tạo văn bản {title}"
    )

    flash('Tạo văn bản thành công')

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

    DocumentModel.delete_document(
        document_id
    )

    AuditLogModel.create_log(
        session['user_id'],
        'DELETE_DOCUMENT',
        'DOCUMENT',
        document_id,
        'Xóa văn bản'
    )

    flash('Đã xóa văn bản')

    return redirect('/admin/documents')


# =========================================================
# ASSIGN DOCUMENT PAGE
# =========================================================
@admin_bp.route(
    '/admin/documents/assign/<int:document_id>',
    methods=['POST']
)
def assign_document(document_id):

    if not check_admin():
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
        'Admin phân công văn bản'
    )

    flash('Đã phân công văn bản')

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

# =========================================================
# SEARCH USERS
# =========================================================
@admin_bp.route('/admin/users/search')
def search_users():

    if not check_admin():
        return redirect('/')

    keyword = request.args.get('keyword')

    users = UserModel.search_users(
        keyword
    )

    return render_template(
        'admin/users.html',
        users=users,
        edit_user=None
    )

# =========================================================
# LOAD USER EDIT
# =========================================================
@admin_bp.route('/admin/users/edit/<int:user_id>')
def load_edit_user(user_id):

    if not check_admin():
        return redirect('/')

    users = UserModel.get_all_users()

    edit_user = UserModel.find_by_id(
        user_id
    )

    return render_template(
        'admin/users.html',
        users=users,
        edit_user=edit_user
    )

# =========================================================
# UPDATE USER
# =========================================================
@admin_bp.route(
    '/admin/users/update/<int:user_id>',
    methods=['POST']
)
def update_user(user_id):

    if not check_admin():
        return redirect('/')

    username = request.form.get('username')
    password = request.form.get('password')

    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    role = request.form.get('role')

    # kiểm tra username trùng
    existing_user = UserModel.find_by_username(username)

    if existing_user and existing_user['id'] != user_id:

        flash('Username đã tồn tại')

        return redirect(f'/admin/users/edit/{user_id}')

    UserModel.update_user(
        user_id,
        username,
        password,
        full_name,
        email,
        phone,
        role
    )

    AuditLogModel.create_log(
        session['user_id'],
        'UPDATE_USER',
        'USER',
        user_id,
        f'Cập nhật user {username}'
    )

    flash('Cập nhật user thành công')

    return redirect('/admin/users')