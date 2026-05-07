# ============================================
# FILE: app/services/auth_service.py
# ============================================

from app.models.user_model import UserModel


class AuthService:
    """
    ==================================
    AUTH SERVICE
    ==================================
    Chứa business logic:
    - Login
    - Register
    - Check role
    """

    @staticmethod
    def login(username, password):

        user = UserModel.find_by_username(username)

        if not user:
            return {
                'success': False,
                'message': 'Sai username!'
            }

        if user['password'] != password:
            return {
                'success': False,
                'message': 'Sai password!'
            }

        return {
            'success': True,
            'user': user
        }

    @staticmethod
    def register(username, password, role):

        if UserModel.user_exists(username):
            return {
                'success': False,
                'message': 'Username đã tồn tại!'
            }

        UserModel.create_user(username, password, role)

        return {
            'success': True,
            'message': 'Đăng ký thành công!'
        }

    @staticmethod
    def check_login(session, role=None):

        if 'user' not in session:
            return False

        if role and session.get('role') != role:
            return False

        return True