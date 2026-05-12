# =========================================================
# FILE: app/models/notification_model.py
# =========================================================

from app.models.database import get_db


class NotificationModel:

    # =====================================================
    # CREATE NOTIFICATION
    # =====================================================
    @staticmethod
    def create_notification(
        user_id,
        title,
        message
    ):

        db = get_db()

        db.execute("""
            INSERT INTO notifications(
                user_id,
                title,
                message
            )
            VALUES (?, ?, ?)
        """, (
            user_id,
            title,
            message
        ))

        db.commit()

    # =====================================================
    # GET USER NOTIFICATIONS
    # =====================================================
    @staticmethod
    def get_user_notifications(user_id):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,)).fetchall()

    # =====================================================
    # MARK AS READ
    # =====================================================
    @staticmethod
    def mark_as_read(notification_id):

        db = get_db()

        db.execute("""
            UPDATE notifications
            SET is_read = 1
            WHERE id = ?
        """, (notification_id,))

        db.commit()

    # =====================================================
    # COUNT UNREAD
    # =====================================================
    @staticmethod
    def count_unread(user_id):

        db = get_db()

        result = db.execute("""
            SELECT COUNT(*) as total
            FROM notifications
            WHERE user_id = ?
            AND is_read = 0
        """, (user_id,)).fetchone()

        return result['total']