# =========================================================
# FILE: app/models/audit_log_model.py
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
        description='',
        ip_address=''
    ):

        db = get_db()

        db.execute("""
            INSERT INTO audit_logs (
                user_id,
                action,
                target_type,
                target_id,
                description,
                ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            action,
            target_type,
            target_id,
            description,
            ip_address
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

                users.username,
                users.full_name

            FROM audit_logs

            LEFT JOIN users
            ON audit_logs.user_id = users.id

            ORDER BY audit_logs.created_at DESC
        """).fetchall()

    # =====================================================
    # GET RECENT LOGS
    # =====================================================
    @staticmethod
    def get_recent_logs(limit=10):

        db = get_db()

        return db.execute("""
            SELECT
                audit_logs.*,

                users.username,
                users.full_name

            FROM audit_logs

            LEFT JOIN users
            ON audit_logs.user_id = users.id

            ORDER BY audit_logs.created_at DESC

            LIMIT ?
        """, (limit,)).fetchall()

    # =====================================================
    # SEARCH LOGS
    # =====================================================
    @staticmethod
    def search_logs(keyword):

        db = get_db()

        return db.execute("""
            SELECT
                audit_logs.*,

                users.username,
                users.full_name

            FROM audit_logs

            LEFT JOIN users
            ON audit_logs.user_id = users.id

            WHERE

                audit_logs.action LIKE ?

                OR audit_logs.description LIKE ?

                OR users.username LIKE ?

                OR users.full_name LIKE ?

            ORDER BY audit_logs.created_at DESC
        """, (
            f'%{keyword}%',
            f'%{keyword}%',
            f'%{keyword}%',
            f'%{keyword}%'
        )).fetchall()

    # =====================================================
    # FILTER LOGS
    # =====================================================
    @staticmethod
    def filter_logs(action=''):

        db = get_db()

        query = """
            SELECT
                audit_logs.*,

                users.username,
                users.full_name

            FROM audit_logs

            LEFT JOIN users
            ON audit_logs.user_id = users.id

            WHERE 1=1
        """

        params = []

        if action:

            query += """
                AND audit_logs.action = ?
            """

            params.append(action)

        query += """
            ORDER BY audit_logs.created_at DESC
        """

        return db.execute(
            query,
            tuple(params)
        ).fetchall()

    # =====================================================
    # COUNT LOGS
    # =====================================================
    @staticmethod
    def count_logs():

        db = get_db()

        result = db.execute("""
            SELECT COUNT(*) as total
            FROM audit_logs
        """).fetchone()

        return result['total']

    # =====================================================
    # DELETE OLD LOGS
    # =====================================================
    @staticmethod
    def delete_old_logs(days=30):

        db = get_db()

        query = """
            DELETE FROM audit_logs
            WHERE created_at <= datetime(
                'now',
                ?
            )
        """

        db.execute(
            query,
            (f'-{int(days)} days',)
        )

        db.commit()