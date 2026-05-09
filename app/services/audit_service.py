# =========================================================
# FILE: app/services/audit_service.py
# =========================================================
# MỤC ĐÍCH:
# - Business logic cho Audit Logs
# - Ghi log hệ thống
# - Lấy lịch sử hoạt động
#
# SERVICE LAYER:
# - Controller gọi Service
# - Service gọi Model
#
# SOLID:
# - SRP:
#   Chỉ xử lý logic Audit
# =========================================================

from flask import request

from app.models.audit_log_model import AuditLogModel


class AuditService:

    # =====================================================
    # WRITE LOG
    # =====================================================
    @staticmethod
    def write_log(
        user_id,
        action,
        target_type='',
        target_id=None,
        description=''
    ):

        ip_address = request.remote_addr

        AuditLogModel.create_log(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            description=description,
            ip_address=ip_address
        )

    # =====================================================
    # GET ALL LOGS
    # =====================================================
    @staticmethod
    def get_all_logs():

        return AuditLogModel.get_all_logs()

    # =====================================================
    # GET LOGS BY USER
    # =====================================================
    @staticmethod
    def get_logs_by_user(user_id):

        return AuditLogModel.get_logs_by_user(user_id)

    # =====================================================
    # GET RECENT LOGS
    # =====================================================
    @staticmethod
    def get_recent_logs(limit=10):

        return AuditLogModel.get_recent_logs(limit)

    # =====================================================
    # DELETE OLD LOGS
    # =====================================================
    @staticmethod
    def delete_old_logs():

        AuditLogModel.delete_old_logs()

        return {
            'success': True,
            'message': 'Đã xóa log cũ!'
        }