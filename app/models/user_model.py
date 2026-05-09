# =========================================================
# FILE: app/models/user_model.py
# =========================================================

from app.models.database import get_db


class UserModel:

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
        phone='',
        department_id=None
    ):

        db = get_db()

        db.execute("""
            INSERT INTO users (
                username,
                password,
                role,
                full_name,
                email,
                phone,
                department_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            password,
            role,
            full_name,
            email,
            phone,
            department_id
        ))

        db.commit()

    # =====================================================
    # FIND BY USERNAME
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
    # FIND BY ID
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
    # USER EXISTS
    # =====================================================
    @staticmethod
    def user_exists(username):

        return UserModel.find_by_username(username) is not None

    # =====================================================
    # GET ALL USERS
    # =====================================================
    @staticmethod
    def get_all_users():

        db = get_db()

        return db.execute("""
            SELECT
                users.*,
                departments.name as department_name
            FROM users

            LEFT JOIN departments
            ON users.department_id = departments.id

            ORDER BY users.created_at DESC
        """).fetchall()

    # =====================================================
    # GET STAFF USERS
    # =====================================================
    @staticmethod
    def get_staff_users():

        db = get_db()

        return db.execute("""
            SELECT *
            FROM users
            WHERE role = 'staff'
        """).fetchall()

    # =====================================================
    # GET MANAGERS
    # =====================================================
    @staticmethod
    def get_managers():

        db = get_db()

        return db.execute("""
            SELECT *
            FROM users
            WHERE role = 'manager'
        """).fetchall()

    # =====================================================
    # SEARCH USERS
    # =====================================================
    @staticmethod
    def search_users(keyword):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM users
            WHERE
                username LIKE ?
                OR full_name LIKE ?
                OR email LIKE ?
        """, (
            f'%{keyword}%',
            f'%{keyword}%',
            f'%{keyword}%'
        )).fetchall()

    # =====================================================
    # UPDATE ROLE
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
    # UPDATE STATUS
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

        # ==============================
        # XÓA LOG LIÊN QUAN USER
        # ==============================
        db.execute("""
            DELETE FROM audit_logs
            WHERE user_id = ?
        """, (user_id,))

        # ==============================
        # GỠ NGƯỜI ĐƯỢC ASSIGN
        # ==============================
        db.execute("""
            UPDATE documents
            SET assigned_to = NULL
            WHERE assigned_to = ?
        """, (user_id,))

        # ==============================
        # GỠ NGƯỜI TẠO DOCUMENT
        # ==============================
        db.execute("""
            UPDATE documents
            SET created_by = NULL
            WHERE created_by = ?
        """, (user_id,))

        # ==============================
        # XÓA USER
        # ==============================
        db.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (user_id,))

        db.commit()

    # =====================================================
    # UPDATE USER FULL INFO
    # =====================================================
    @staticmethod
    def update_user(
        user_id,
        username,
        password,
        full_name,
        email,
        phone,
        role
    ):

        db = get_db()

        db.execute("""
            UPDATE users
            SET
                username = ?,
                password = ?,
                full_name = ?,
                email = ?,
                phone = ?,
                role = ?
            WHERE id = ?
        """, (
            username,
            password,
            full_name,
            email,
            phone,
            role,
            user_id
        ))

        db.commit()