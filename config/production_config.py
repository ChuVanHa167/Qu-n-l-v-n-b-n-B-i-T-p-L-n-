# =========================================================
# FILE: config/production_config.py
# =========================================================

"""
Production Config
-----------------
Môi trường production thực tế.

Dùng khi:
- deploy server
- chạy thật

ĐẶC ĐIỂM:
- tắt debug
- bảo mật cao hơn
- tối ưu performance
"""

import os


class ProductionConfig:

    # =====================================================
    # FLASK CORE
    # =====================================================
    DEBUG = False

    TESTING = False

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "production_secret_key"
    )

    # =====================================================
    # DATABASE
    # =====================================================
    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    DATABASE = os.path.join(
        BASE_DIR,
        "..",
        "database",
        "production.db"
    )

    # =====================================================
    # SESSION
    # =====================================================
    SESSION_PERMANENT = True

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = True

    # =====================================================
    # SECURITY
    # =====================================================
    WTF_CSRF_ENABLED = True

    # =====================================================
    # APP INFO
    # =====================================================
    APP_NAME = "Document Management System"

    APP_VERSION = "1.0 Production"

    # =====================================================
    # PAGINATION
    # =====================================================
    USERS_PER_PAGE = 20

    DOCUMENTS_PER_PAGE = 20

    # =====================================================
    # FILE UPLOAD
    # =====================================================
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024

    UPLOAD_FOLDER = "app/static/uploads"

    # =====================================================
    # LOGGING
    # =====================================================
    LOG_LEVEL = "ERROR"