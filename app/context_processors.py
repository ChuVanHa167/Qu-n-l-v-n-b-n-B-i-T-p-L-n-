from flask import session

from app.models.notification_model import (
    NotificationModel
)

def inject_notifications():

    unread_count = 0

    if 'user_id' in session:

        unread_count = (
            NotificationModel.count_unread(
                session['user_id']
            )
        )

    return dict(
        unread_count=unread_count
    )