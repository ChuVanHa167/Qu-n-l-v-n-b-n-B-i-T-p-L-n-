# =========================================================
# FILE: app/models/user_model.py
# =========================================================
# MỤC ĐÍCH:
# - Quản lý toàn bộ dữ liệu USERS
#
# NGUYÊN TẮC:
# - Model chỉ thao tác DB
# - Không xử lý business logic
# - Không render giao diện
#
# SOLID:
# - SRP:
#   File này CHỈ xử lý user
#
# - OCP:
#   Có thể thêm method mới
#   mà không phá code cũ
# =========================================================

from app.models.database import get_db


class UserModel:

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

        db = get_db()

        db.execute("""
            INSERT INTO users (
                username,
                password,
                role,
                full_name,
                email,
                phone
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            password,
            role,
            full_name,
            email,
            phone
        ))

        db.commit()

    # =====================================================
    # FIND USER BY USERNAME
    # =====================================================
    @staticmethod
    def find_by_username(username):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (username,)).fetchone()

    # =====================================================
    # FIND USER BY ID
    # =====================================================
    @staticmethod
    def find_by_id(user_id):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM users
            WHERE id = ?
        """, (user_id,)).fetchone()

    # =====================================================
    # CHECK USER EXISTS
    # =====================================================
    @staticmethod
    def user_exists(username):

        user = UserModel.find_by_username(username)

        return user is not None

    # =====================================================
    # GET ALL USERS
    # =====================================================
    @staticmethod
    def get_all_users():

        db = get_db()

        return db.execute("""
            SELECT *
            FROM users
            ORDER BY created_at DESC
        """).fetchall()

    # =====================================================
    # UPDATE USER ROLE
    # =====================================================
    @staticmethod
    def update_role(user_id, role):

        db = get_db()

        db.execute("""
            UPDATE users
            SET role = ?
            WHERE id = ?
        """, (
            role,
            user_id
        ))

        db.commit()

    # =====================================================
    # UPDATE USER STATUS
    # =====================================================
    @staticmethod
    def update_status(user_id, is_active):

        db = get_db()

        db.execute("""
            UPDATE users
            SET is_active = ?
            WHERE id = ?
        """, (
            is_active,
            user_id
        ))

        db.commit()

    # =====================================================
    # DELETE USER
    # =====================================================
    @staticmethod
    def delete_user(user_id):

        db = get_db()

        db.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (user_id,))

        db.commit()

    # =====================================================
    # COUNT USERS
    # =====================================================
    @staticmethod
    def count_users():

        db = get_db()

        result = db.execute("""
            SELECT COUNT(*) as total
            FROM users
        """).fetchone()

        return result['total']