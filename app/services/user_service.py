# =========================================================
# FILE: app/services/user_service.py
# =========================================================
# MỤC ĐÍCH:
# - Business logic cho User
#
# CHỨC NĂNG:
# - CRUD User
# - Role management
# - User statistics
#
# SOLID:
# - Chỉ xử lý user logic
# =========================================================

from app.models.user_model import UserModel


class UserService:

    # =====================================================
    # GET ALL USERS
    # =====================================================
    @staticmethod
    def get_all_users():

        return UserModel.get_all_users()

    # =====================================================
    # GET USER BY ID
    # =====================================================
    @staticmethod
    def get_user_by_id(user_id):

        user = UserModel.find_by_id(user_id)

        if not user:

            return {
                'success': False,
                'message': 'User không tồn tại!'
            }

        return {
            'success': True,
            'user': user
        }

    # =====================================================
    # CREATE USER
    # =====================================================
    @staticmethod
    def create_user(
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

        # check username
        if UserModel.user_exists(username):

            return {
                'success': False,
                'message': 'Username đã tồn tại!'
            }

        # validate role
        valid_roles = [
            'admin',
            'staff',
            'employee'
        ]

        if role not in valid_roles:

            return {
                'success': False,
                'message': 'Role không hợp lệ!'
            }

        # create user
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
            'message': 'Tạo user thành công!'
        }

    # =====================================================
    # UPDATE USER ROLE
    # =====================================================
    @staticmethod
    def update_user_role(user_id, role):

        UserModel.update_role(user_id, role)

        return {
            'success': True,
            'message': 'Cập nhật role thành công!'
        }

    # =====================================================
    # UPDATE USER STATUS
    # =====================================================
    @staticmethod
    def update_user_status(
        user_id,
        is_active
    ):

        UserModel.update_status(
            user_id,
            is_active
        )

        return {
            'success': True,
            'message': 'Cập nhật trạng thái thành công!'
        }

    # =====================================================
    # DELETE USER
    # =====================================================
    @staticmethod
    def delete_user(user_id):

        user = UserModel.find_by_id(user_id)

        if not user:

            return {
                'success': False,
                'message': 'User không tồn tại!'
            }

        UserModel.delete_user(user_id)

        return {
            'success': True,
            'message': 'Xóa user thành công!'
        }

    # =====================================================
    # COUNT USERS
    # =====================================================
    @staticmethod
    def count_users():

        return UserModel.count_users()

    # =====================================================
    # COUNT ACTIVE USERS
    # =====================================================
    @staticmethod
    def count_active_users():

        return UserModel.count_active_users()

    # =====================================================
    # COUNT INACTIVE USERS
    # =====================================================
    @staticmethod
    def count_inactive_users():

        return UserModel.count_inactive_users()