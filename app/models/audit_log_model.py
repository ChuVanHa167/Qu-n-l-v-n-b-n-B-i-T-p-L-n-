# =========================================================
# FILE: app/models/audit_log_model.py
# =========================================================
# MỤC ĐÍCH:
# - Ghi lịch sử thao tác hệ thống
#
# Ví dụ:
# - Admin tạo user
# - Staff xử lý văn bản
# - User đăng nhập
#
# LỢI ÍCH:
# - Theo dõi hệ thống
# - Audit
# - Debug
# - Security
# =========================================================

from app.models.database import get_db


class AuditLogModel:

    # =====================================================
    # CREATE LOG
    # =====================================================
    @staticmethod
    def create_log(
        user_id,
        action,
        target_type='',
        target_id=None,
        description=''
    ):

        db = get_db()

        db.execute("""
            INSERT INTO audit_logs (
                user_id,
                action,
                target_type,
                target_id,
                description
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            action,
            target_type,
            target_id,
            description
        ))

        db.commit()

    # =====================================================
    # GET ALL LOGS
    # =====================================================
    @staticmethod
    def get_all_logs():

        db = get_db()

        return db.execute("""
            SELECT
                audit_logs.*,
                users.username
            FROM audit_logs

            LEFT JOIN users
            ON audit_logs.user_id = users.id

            ORDER BY audit_logs.created_at DESC
        """).fetchall()

    # =====================================================
    # GET LOGS BY USER
    # =====================================================
    @staticmethod
    def get_logs_by_user(user_id):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM audit_logs
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,)).fetchall()

    # =====================================================
    # DELETE OLD LOGS
    # =====================================================
    @staticmethod
    def delete_old_logs():

        db = get_db()

        db.execute("""
            DELETE FROM audit_logs
            WHERE created_at <= datetime('now', '-30 days')
        """)

        db.commit()