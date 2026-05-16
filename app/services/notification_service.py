# =========================================================
# FILE: app/services/notification_service.py
# =========================================================

from app.models.notification_model import (
    NotificationModel
)


class NotificationService:

    @classmethod
    def notify(
        cls,
        user_id,
        title,
        message
    ):

        NotificationModel.create_notification(
            user_id,
            title,
            message
        )