# ============================================
# FILE: app/services/user_service.py
# ============================================

from app.models.user_model import UserModel


class UserService:
    """
    ==================================
    USER SERVICE
    ==================================
    Xử lý logic nghiệp vụ User
    """

    @staticmethod
    def get_all_users():

        return UserModel.get_all_users()

    @staticmethod
    def create_user(username, password, role):

        if not username or not password:
            return {
                'success': False,
                'message': 'Thiếu dữ liệu!'
            }

        if UserModel.user_exists(username):
            return {
                'success': False,
                'message': 'Username đã tồn tại!'
            }

        UserModel.create_user(username, password, role)

        return {
            'success': True,
            'message': 'Tạo user thành công!'
        }

    @staticmethod
    def delete_user(user_id):

        UserModel.delete_user(user_id)

        return {
            'success': True,
            'message': 'Xóa user thành công!'
        }

    @staticmethod
    def update_user_role(user_id, role):

        UserModel.update_role(user_id, role)

        return {
            'success': True,
            'message': 'Cập nhật role thành công!'
        }

    @staticmethod
    def count_users():

        return UserModel.count_users()