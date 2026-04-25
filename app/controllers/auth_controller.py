from flask import Blueprint, render_template, request, redirect, session
from app.models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)

# LOGIN
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = UserModel.find_by_username(username)

        if not user:
            return "Sai username!"

        if user['password'] != password:
            return "Sai password!"

        session['user'] = user['username']
        session['role'] = user['role']

        if user['role'] == 'admin':
            return redirect('/admin')
        elif user['role'] == 'staff':
            return redirect('/staff')
        else:
            return redirect('/user')

    return render_template('auth/login.html')


# REGISTER
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if UserModel.user_exists(username):
            return "Username đã tồn tại!"

        UserModel.create_user(username, password, role)
        return redirect('/')

    return render_template('auth/register.html')


# LOGOUT
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# DASHBOARD
@auth_bp.route('/admin')
def admin():
    if not check_login('admin'):
        return redirect('/')
    return render_template('dashboard/admin.html')


@auth_bp.route('/staff')
def staff():
    if not check_login('staff'):
        return redirect('/')
    return render_template('dashboard/staff.html')


@auth_bp.route('/user')
def user():
    if not check_login():
        return redirect('/')
    return render_template('dashboard/user.html')


def check_login(role=None):
    if 'user' not in session:
        return False

    if role and session.get('role') != role:
        return False

    return True