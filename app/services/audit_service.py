# ============================================
# FILE: app/services/audit_service.py
# ============================================

from app.models.audit_log_model import AuditLogModel


class AuditService:
    """
    ==================================
    AUDIT SERVICE
    ==================================
    Xử lý log hệ thống
    """

    @staticmethod
    def write_log(username, action, target):

        AuditLogModel.create_log(
            username,
            action,
            target
        )

    @staticmethod
    def get_all_logs():

        return AuditLogModel.get_all_logs()

    @staticmethod
    def get_recent_logs(limit=10):

        return AuditLogModel.get_recent_logs(limit)