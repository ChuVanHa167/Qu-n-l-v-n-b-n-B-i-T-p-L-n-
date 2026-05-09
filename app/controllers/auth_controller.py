# =========================================================
# FILE: app/controllers/auth_controller.py
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash

from app.models.user_model import UserModel
from app.models.audit_log_model import AuditLogModel


auth_bp = Blueprint(
    'auth',
    __name__
)


# =========================================================
# CHECK LOGIN
# =========================================================
def check_login(role=None):

    if 'user_id' not in session:
        return False

    if role and session.get('role') != role:
        return False

    return True


# =========================================================
# LOGIN
# =========================================================
@auth_bp.route('/', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form.get(
            'username'
        )

        password = request.form.get(
            'password'
        )

        user = UserModel.find_by_username(
            username
        )

        # user không tồn tại
        if not user:

            error = "Sai username"

        # tài khoản bị khóa
        elif user['is_active'] == 0:

            error = "Tài khoản đã bị khóa"

        # sai password
        elif user['password'] != password:

            error = "Sai password"

        else:

            # lưu session
            session['user_id'] = user['id']

            session['username'] = user[
                'username'
            ]

            session['role'] = user[
                'role'
            ]

            # ghi audit log
            AuditLogModel.create_log(
                user['id'],
                'LOGIN',
                'USER',
                user['id'],
                f"{user['username']} đăng nhập hệ thống"
            )

            flash('Đăng nhập thành công')

            # điều hướng theo role
            if user['role'] == 'admin':

                return redirect('/admin')

            elif user['role'] == 'staff':

                return redirect('/staff')

            else:

                return redirect('/employee')

    return render_template(
        'auth/login.html',
        error=error
    )


# =========================================================
# REGISTER
# =========================================================
@auth_bp.route(
    '/register',
    methods=['GET', 'POST']
)
def register():

    error = None

    if request.method == 'POST':

        username = request.form.get(
            'username'
        )

        password = request.form.get(
            'password'
        )

        role = request.form.get(
            'role'
        )

        full_name = request.form.get(
            'full_name'
        )

        email = request.form.get(
            'email'
        )

        phone = request.form.get(
            'phone'
        )

        # check user tồn tại
        if UserModel.user_exists(username):

            error = "Username đã tồn tại"

        else:

            UserModel.create_user(
                username,
                password,
                role,
                full_name,
                email,
                phone
            )

            flash('Đăng ký thành công')

            return redirect('/')

    return render_template(
        'auth/register.html',
        error=error
    )


# =========================================================
# LOGOUT
# =========================================================
@auth_bp.route('/logout')
def logout():

    # ghi log trước khi clear session
    if 'user_id' in session:

        AuditLogModel.create_log(
            session['user_id'],
            'LOGOUT',
            'USER',
            session['user_id'],
            'Đăng xuất hệ thống'
        )

    session.clear()

    flash('Đã đăng xuất')

    return redirect('/')