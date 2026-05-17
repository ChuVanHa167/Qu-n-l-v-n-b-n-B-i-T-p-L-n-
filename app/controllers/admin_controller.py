# =========================================================
# FILE: app/controllers/admin_controller.py
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash
from app.models.notification_model import (
    NotificationModel
)
from app.models.settings_model import SettingsModel
from app.models.audit_log_model import AuditLogModel
from app.models.user_model import UserModel
from app.models.document_model import DocumentModel
from app.services.audit_service import AuditService
from app.services.ai.document_ai_service import (
    DocumentAIService
)
import app.services.notification_service as ns
import uuid
import os

from werkzeug.utils import secure_filename

from flask import current_app
from flask import jsonify
from functools import wraps
from flask import abort

admin_bp = Blueprint(
    'admin',
    __name__
)

# =========================================================
# ALLOWED FILE EXTENSIONS
# =========================================================
ALLOWED_EXTENSIONS = {
    'pdf',
    'docx',
    'png',
    'jpg',
    'jpeg'
}


def allowed_file(filename):

    return (
        '.' in filename
        and
        filename.rsplit('.', 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# ROLE CHECK
# =========================================================
def roles_required(*roles):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            if 'user_id' not in session:
                return redirect('/')

            user_role = session.get('role')

            if user_role not in roles:
                abort(403)

            return f(*args, **kwargs)

        return wrapper

    return decorator


# =========================================================
# ADMIN CHECK
# =========================================================
def check_admin():

    if 'user_id' not in session:
        return False

    return session.get('role') == 'admin'


# =========================================================
# ADMIN DASHBOARD
# =========================================================
@admin_bp.route('/admin')
@admin_bp.route('/admin/index')
@roles_required('admin', 'manager')
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

    overdue_documents = (
        DocumentModel.get_overdue_documents()
    )

    recent_documents = DocumentModel.get_recent_documents()

    recent_logs = AuditService.get_recent_logs()

    notifications = NotificationModel.get_user_notifications(
        session['user_id']
    )

    unread_count = NotificationModel.count_unread(
        session['user_id']
    )

    return render_template(
        'admin/dashboard.html',

        total_users=total_users,
        total_documents=total_documents,

        pending_documents=pending_documents,
        processing_documents=processing_documents,
        approved_documents=approved_documents,
        rejected_documents=rejected_documents,
        overdue_documents=overdue_documents,
        recent_documents=recent_documents,
        recent_logs=recent_logs,
        notifications=notifications,
        unread_count=unread_count
    )


# =========================================================
# USERS PAGE
# =========================================================
@admin_bp.route('/admin/users')
@roles_required('admin')
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
@roles_required('admin')
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

        AuditService.write_log(
            user_id=session['user_id'],
            action='CREATE_USER',
            target_type='USER',
            description=f'Tạo user {username}'
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
@roles_required('admin')
def update_user_role(user_id):

    if not check_admin():
        return redirect('/')

    role = request.form.get('role')

    UserModel.update_role(
        user_id,
        role
    )

    AuditService.write_log(
        user_id=session['user_id'],
        action='UPDATE_USER_ROLE',
        target_type='USER',
        target_id=user_id,
        description=f'Cập nhật role thành {role}'
    )

    return redirect('/admin/users')


# =========================================================
# UPDATE USER STATUS
# =========================================================
@admin_bp.route(
    '/admin/users/update-status/<int:user_id>'
)
@roles_required('admin')
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

    AuditService.write_log(
        user_id=session['user_id'],
        action='UPDATE_USER_STATUS',
        target_type='USER',
        target_id=user_id,
        description='Cập nhật trạng thái tài khoản'
    )

    return redirect('/admin/users')


# =========================================================
# DELETE USER
# =========================================================
@admin_bp.route('/admin/users/delete/<int:user_id>')
@roles_required('admin')
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
    AuditService.write_log(
        user_id=session['user_id'],
        action='DELETE_USER',
        target_type='USER',
        target_id=user_id,
        description=f'Admin đã xóa user {username}'
    )

    flash('Xóa user thành công')

    return redirect('/admin/users')


# =========================================================
# DOCUMENT PAGE
# =========================================================
@admin_bp.route('/admin/documents')
@roles_required('admin', 'manager')
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
@roles_required('admin', 'manager')
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

    # =====================================================
    # FILE UPLOAD
    # =====================================================
    uploaded_file = request.files.get(
        'document_file'
    )

    file_path = ''

    original_filename = ''

    if uploaded_file and uploaded_file.filename != '':

        # check extension
        if not allowed_file(uploaded_file.filename):

            flash('File không hợp lệ')

            return redirect('/admin/documents')

        original_filename = secure_filename(
            uploaded_file.filename
        )

        filename = (
            f"{uuid.uuid4()}_{original_filename}"
        )
        upload_folder = current_app.config[
            'UPLOAD_FOLDER'
        ]

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        save_path = os.path.join(
            upload_folder,
            filename
        )

        uploaded_file.save(save_path)

        file_path = save_path

        original_filename = filename

    # =====================================================
    # CREATE DOCUMENT
    # =====================================================
    DocumentModel.create_document(
        title=title,
        content=content,
        document_type=document_type,
        category=category,
        priority=priority,
        file_path=file_path,
        original_filename=original_filename,
        created_by=session['user_id']
    )

    AuditService.write_log(
        user_id=session['user_id'],
        action='CREATE_DOCUMENT',
        target_type='DOCUMENT',
        description=f'Tạo văn bản {title}'
    )

    flash('Tạo văn bản thành công')

    return redirect('/admin/documents')


# =========================================================
# DELETE DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/delete/<int:document_id>'
)
@roles_required('admin')
def delete_document(document_id):

    if not check_admin():
        return redirect('/')

    DocumentModel.delete_document(
        document_id,
        session['user_id']
    )

    AuditService.write_log(
        user_id=session['user_id'],
        action='DELETE_DOCUMENT',
        target_type='DOCUMENT',
        target_id=document_id,
        description='Xóa văn bản'
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
@roles_required('admin', 'manager')
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

    ns.NotificationService.notify(
        assigned_to,
        '📄 Văn bản mới',
        'Bạn được phân công xử lý văn bản mới'
    )

    AuditService.write_log(
        user_id=session['user_id'],
        action='ASSIGN_DOCUMENT',
        target_type='DOCUMENT',
        target_id=document_id,
        description='Admin phân công văn bản'
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

    logs = AuditService.get_all_logs()

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

    system_name = SettingsModel.get_setting(
        'system_name'
    )

    admin_email = SettingsModel.get_setting(
        'admin_email'
    )

    ocr_engine = SettingsModel.get_setting(
        'ocr_engine'
    )

    return render_template(
        'admin/settings.html',

        system_name=system_name,
        admin_email=admin_email,
        ocr_engine=ocr_engine
    )

# =========================================================
# UPDATE SETTINGS
# =========================================================
@admin_bp.route(
    '/admin/settings/update',
    methods=['POST']
)
def update_settings():

    if not check_admin():
        return redirect('/')

    system_name = request.form.get(
        'system_name'
    )

    admin_email = request.form.get(
        'admin_email'
    )

    ocr_engine = request.form.get(
        'ocr_engine'
    )

    SettingsModel.set_setting(
        'system_name',
        system_name
    )

    SettingsModel.set_setting(
        'admin_email',
        admin_email
    )

    SettingsModel.set_setting(
        'ocr_engine',
        ocr_engine
    )

    flash('Cập nhật settings thành công')

    return redirect('/admin/settings')

# =========================================================
# SEARCH USERS
# =========================================================
@admin_bp.route('/admin/users/search')
@roles_required('admin')
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

@roles_required('admin')
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

    AuditService.write_log(
        user_id=session['user_id'],
        action='UPDATE_USER',
        target_type='USER',
        target_id=user_id,
        description=f'Cập nhật user {username}'
    )

    flash('Cập nhật user thành công')

    return redirect('/admin/users')

# =========================================================
# WORKFLOW DETAIL
# =========================================================
@admin_bp.route(
    '/admin/documents/workflow/<int:document_id>'
)
def workflow_detail(document_id):

    if not check_admin():
        return redirect('/')

    document = DocumentModel.get_document_full_detail(
        document_id
    )

    comments = DocumentModel.get_document_comments(
        document_id
    )

    histories = DocumentModel.get_approval_history(
        document_id
    )

    users = UserModel.get_all_users()

    return render_template(
        'admin/workflow_detail.html',

        document=document,
        comments=comments,
        histories=histories,
        users=users
    )

# =========================================================
# FILTER DOCUMENTS
# =========================================================
@admin_bp.route('/admin/documents/filter')
def filter_documents():

    if not check_admin():
        return redirect('/')

    keyword = request.args.get(
        'keyword',
        ''
    )

    status = request.args.get(
        'status',
        ''
    )

    document_type = request.args.get(
        'document_type',
        ''
    )

    documents = DocumentModel.filter_documents(
        keyword,
        status,
        document_type
    )

    users = UserModel.get_all_users()

    return render_template(
        'admin/documents.html',

        documents=documents,
        users=users
    )

# =========================================================
# LOAD EDIT DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/edit/<int:document_id>'
)
def load_edit_document(document_id):

    if not check_admin():
        return redirect('/')

    documents = DocumentModel.get_all_documents()

    users = UserModel.get_all_users()

    edit_document = DocumentModel.get_document_by_id(
        document_id
    )

    return render_template(
        'admin/documents.html',

        documents=documents,
        users=users,

        # truyền document edit xuống view
        edit_document=edit_document
    )


# =========================================================
# UPDATE DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/update/<int:document_id>',
    methods=['POST']
)
@roles_required('admin', 'manager')
def update_document(document_id):

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

    DocumentModel.update_document(
        document_id,
        title,
        content,
        document_type,
        category,
        priority
    )

    # log audit
    AuditService.write_log(
        user_id=session['user_id'],
        action='UPDATE_DOCUMENT',
        target_type='DOCUMENT',
        target_id=document_id,
        description=f'Cập nhật văn bản {title}'
    )

    flash('Cập nhật văn bản thành công')

    return redirect('/admin/documents')

# =========================================================
# PROCESS AI DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/process-ai/<int:document_id>'
)
@roles_required('admin', 'manager')
def process_ai_document(document_id):

    if not check_admin():
        return redirect('/')

    # lấy document
    document = DocumentModel.get_document_by_id(
        document_id
    )

    if not document:

        flash('Document không tồn tại')

        return redirect('/admin/documents')

    # chưa upload file
    if not document['file_path']:

        flash('Document chưa có file upload')

        return redirect('/admin/documents')

    # process AI local
    ai_result = DocumentAIService.process_document(
        document['file_path']
    )

    # save db
    DocumentModel.save_ai_processing_result(
        document_id=document_id,

        ocr_text=ai_result['ocr_text'],

        ai_summary=ai_result['summary'],

        ai_category=ai_result['category']
    )

    # audit log
    AuditService.write_log(
        user_id=session['user_id'],
        action='PROCESS_AI_DOCUMENT',
        target_type='DOCUMENT',
        target_id=document_id,
        description='AI xử lý văn bản'
    )

    flash('AI xử lý văn bản thành công')

    return redirect('/admin/documents')

# =========================================================
# AI AUTO EXTRACT
# =========================================================
@admin_bp.route(
    '/admin/documents/ai-extract',
    methods=['POST']
)
@roles_required('admin', 'manager')
def ai_extract_document():

    if not check_admin():
        return jsonify({
            "success": False
        })

    file = request.files.get('file')

    if not file:

        return jsonify({
            "success": False,
            "message": "Không có file"
        })
    if not allowed_file(file.filename):

        return jsonify({
            "success": False,
            "message": "File không hợp lệ"
        })

    # =====================================================
    # SAVE FILE
    # =====================================================
    upload_folder = current_app.config[
        'UPLOAD_FOLDER'
    ]

    os.makedirs(upload_folder, exist_ok=True)

    original_filename = secure_filename(
        file.filename
    )

    filename = (
        f"{uuid.uuid4()}_{original_filename}"
    )

    file_path = os.path.join(
        upload_folder,
        filename
    )

    file.save(file_path)

    # =====================================================
    # AI PROCESS
    # =====================================================
    ai_result = DocumentAIService.process_document(
        file_path
    )

    ai_result['file_path'] = file_path

    ai_result['original_filename'] = filename

    return jsonify({
        "success": True,
        "data": ai_result
    })

# =========================================================
# SEARCH AUDIT LOGS
# =========================================================
@admin_bp.route('/admin/audit/search')
def search_audit_logs():

    if not check_admin():
        return redirect('/')

    keyword = request.args.get(
        'keyword',
        ''
    )

    logs = AuditLogModel.search_logs(keyword)

    return render_template(
        'admin/audit_logs.html',
        logs=logs
    )

# =========================================================
# FILTER AUDIT LOGS
# =========================================================
@admin_bp.route('/admin/audit/filter')
def filter_audit_logs():

    if not check_admin():
        return redirect('/')

    action = request.args.get(
        'action',
        ''
    )

    logs = AuditLogModel.filter_logs(action)

    return render_template(
        'admin/audit_logs.html',
        logs=logs
    )

# =========================================================
# APPROVE DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/approve/<int:document_id>'
)
@roles_required('admin')
def approve_document(document_id):

    if not check_admin():
        return redirect('/')

    DocumentModel.update_document_status(
        document_id,
        'approved'
    )

    DocumentModel.create_approval_history(
        document_id,
        'APPROVED',
        'Duyệt văn bản',
        session['user_id']
    )

    AuditService.write_log(
        user_id=session['user_id'],
        action='APPROVE_DOCUMENT',
        target_type='DOCUMENT',
        target_id=document_id,
        description='Duyệt văn bản'
    )

    flash('Đã duyệt văn bản')

    return redirect(
        f'/admin/documents/workflow/{document_id}'
    )

# =========================================================
# REJECT DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/reject/<int:document_id>',
    methods=['POST']
)
@roles_required('admin', 'manager')
def reject_document(document_id):

    if not check_admin():
        return redirect('/')

    reason = request.form.get('reason')

    DocumentModel.reject_document(
        document_id,
        reason
    )

    DocumentModel.create_approval_history(
        document_id,
        'REJECTED',
        reason,
        session['user_id']
    )

    AuditService.write_log(
        user_id=session['user_id'],
        action='REJECT_DOCUMENT',
        target_type='DOCUMENT',
        target_id=document_id,
        description='Từ chối văn bản'
    )

    flash('Đã từ chối văn bản')

    return redirect(
        f'/admin/documents/workflow/{document_id}'
    )

# =========================================================
# COMMENT DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/comment/<int:document_id>',
    methods=['POST']
)
def comment_document(document_id):

    if not check_admin():
        return redirect('/')

    comment = request.form.get('comment')

    DocumentModel.add_comment(
        document_id,
        session['user_id'],
        comment
    )

    DocumentModel.create_approval_history(
        document_id,
        'COMMENT',
        comment,
        session['user_id']
    )

    flash('Đã thêm bình luận')

    return redirect(
        f'/admin/documents/workflow/{document_id}'
    )

# =========================================================
# NOTIFICATIONS PAGE
# =========================================================
@admin_bp.route('/notifications')
def notifications_page():

    if 'user_id' not in session:
        return redirect('/')

    notifications = (
        NotificationModel.get_user_notifications(
            session['user_id']
        )
    )

    unread_count = NotificationModel.count_unread(
        session['user_id']
    )

    return render_template(
        'admin/notifications.html',
        notifications=notifications,
        unread_count=unread_count
    )

# =========================================================
# MARK NOTIFICATION AS READ
# =========================================================
@admin_bp.route(
    '/notifications/read/<int:notification_id>'
)
def mark_notification_read(notification_id):

    if 'user_id' not in session:
        return redirect('/')

    NotificationModel.mark_as_read(
        notification_id
    )

    return redirect('/notifications')

# =========================================================
# 403 ERROR
# =========================================================
@admin_bp.app_errorhandler(403)
def forbidden(e):

    return render_template(
        'errors/403.html'
    ), 403

# =========================================================
# RECYCLE BIN
# =========================================================
@admin_bp.route('/admin/recycle-bin')
@roles_required('admin')
def recycle_bin():

    documents = DocumentModel.get_deleted_documents()

    return render_template(
        'admin/recycle_bin.html',
        documents=documents
    )

# =========================================================
# RESTORE DOCUMENT
# =========================================================
@admin_bp.route(
    '/admin/documents/restore/<int:document_id>'
)
@roles_required('admin')
def restore_document(document_id):

    DocumentModel.restore_document(
        document_id
    )

    flash('Khôi phục thành công')

    return redirect('/admin/recycle-bin')

# =========================================================
# VERSION HISTORY
# =========================================================
@admin_bp.route(
    '/admin/documents/versions/<int:document_id>'
)
@roles_required('admin', 'manager')
def document_versions(document_id):

    versions = (
        DocumentModel.get_document_versions(
            document_id
        )
    )

    document = (
        DocumentModel.get_document_by_id(
            document_id
        )
    )

    return render_template(
        'admin/document_versions.html',

        versions=versions,
        document=document
    )