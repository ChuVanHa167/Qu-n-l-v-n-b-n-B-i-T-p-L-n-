# =========================================================
# FILE: app/models/audit_log_model.py
# =========================================================

from app.models.database import get_db


class AuditLogModel:

    # =====================================================
    # GET RECENT LOGS
    # =====================================================
    @staticmethod
    def get_recent_logs(limit=10):

        db = get_db()

        return db.execute("""
            SELECT
                audit_logs.*,
                users.username
            FROM audit_logs

            LEFT JOIN users
            ON audit_logs.user_id = users.id

            ORDER BY audit_logs.created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()

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
    # SEARCH LOGS
    # =====================================================
    @staticmethod
    def search_logs(keyword):

        db = get_db()

        return db.execute("""
            SELECT
                audit_logs.*,
                users.username
            FROM audit_logs

            LEFT JOIN users
            ON audit_logs.user_id = users.id

            WHERE
                audit_logs.action LIKE ?
                OR audit_logs.description LIKE ?
                OR users.username LIKE ?

            ORDER BY audit_logs.created_at DESC
        """, (
            f'%{keyword}%',
            f'%{keyword}%',
            f'%{keyword}%'
        )).fetchall()

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
    def delete_old_logs(days=30):

        db = get_db()

        db.execute(f"""
            DELETE FROM audit_logs
            WHERE created_at <= datetime(
                'now',
                '-{days} days'
            )
        """)

        db.commit()