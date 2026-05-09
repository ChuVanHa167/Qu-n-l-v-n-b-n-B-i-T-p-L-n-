# =========================================================
# FILE: app/services/auth_service.py
# =========================================================
# MỤC ĐÍCH:
# - Xử lý business logic Authentication
#
# CHỨC NĂNG:
# - Login
# - Register
# - Check session
#
# SECURITY:
# - Check user active
# - Validate dữ liệu
# =========================================================

from app.models.user_model import UserModel


class AuthService:

    # =====================================================
    # LOGIN
    # =====================================================
    @staticmethod
    def login(username, password):

        # validate input
        if not username or not password:

            return {
                'success': False,
                'message': 'Thiếu username hoặc password!'
            }

        user = UserModel.find_by_username(username)

        # user không tồn tại
        if not user:

            return {
                'success': False,
                'message': 'Sai username!'
            }

        # tài khoản bị khóa
        if user['is_active'] == 0:

            return {
                'success': False,
                'message': 'Tài khoản đã bị khóa!'
            }

        # sai mật khẩu
        if user['password'] != password:

            return {
                'success': False,
                'message': 'Sai password!'
            }

        return {
            'success': True,
            'user': user
        }

    # =====================================================
    # REGISTER
    # =====================================================
    @staticmethod
    def register(
        username,
        password,
        role,
        full_name='',
        email='',
        phone=''
    ):

        # validate
        if not username or not password:

            return {
                'success': False,
                'message': 'Thiếu dữ liệu!'
            }

        # check tồn tại
        if UserModel.user_exists(username):

            return {
                'success': False,
                'message': 'Username đã tồn tại!'
            }

        # tạo user
        UserModel.create_user(
            username=username,
            password=password,
            role=role,
            full_name=full_name,
            email=email,
            phone=phone
        )

        return {
            'success': True,
            'message': 'Đăng ký thành công!'
        }

    # =====================================================
    # CHECK LOGIN
    # =====================================================
    @staticmethod
    def check_login(session, role=None):

        # chưa login
        if 'user_id' not in session:
            return False

        # check role
        if role:

            if session.get('role') != role:
                return False

        return True

    # =====================================================
    # CHECK ADMIN
    # =====================================================
    @staticmethod
    def is_admin(session):

        return (
            'user_id' in session and
            session.get('role') == 'admin'
        )

    # =====================================================
    # CHECK STAFF
    # =====================================================
    @staticmethod
    def is_staff(session):

        return (
            'user_id' in session and
            session.get('role') == 'staff'
        )

    # =====================================================
    # CHECK EMPLOYEE
    # =====================================================
    @staticmethod
    def is_employee(session):

        return (
            'user_id' in session and
            session.get('role') == 'employee'
        )