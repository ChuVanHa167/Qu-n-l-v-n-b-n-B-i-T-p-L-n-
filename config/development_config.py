# =========================================================
# FILE: config/development_config.py
# =========================================================

"""
Development Config
------------------
Môi trường phát triển local.

Dùng khi:
- code local
- debug
- test giao diện
- test database

ĐẶC ĐIỂM:
- DEBUG bật
- reload tự động
- log chi tiết
"""

import os


class DevelopmentConfig:

    # =====================================================
    # FLASK CORE
    # =====================================================
    DEBUG = True

    TESTING = False

    SECRET_KEY = "dev_secret_key"

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
        "development.db"
    )

    # =====================================================
    # SESSION
    # =====================================================
    SESSION_PERMANENT = False

    SESSION_COOKIE_HTTPONLY = True

    # =====================================================
    # SECURITY
    # =====================================================
    WTF_CSRF_ENABLED = False

    # =====================================================
    # APP INFO
    # =====================================================
    APP_NAME = "Document Management System"

    APP_VERSION = "1.0 Development"

    # =====================================================
    # PAGINATION
    # =====================================================
    USERS_PER_PAGE = 10

    DOCUMENTS_PER_PAGE = 10

    # =====================================================
    # FILE UPLOAD
    # =====================================================
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    UPLOAD_FOLDER = "app/static/uploads"

    # =====================================================
    # LOGGING
    # =====================================================
    LOG_LEVEL = "DEBUG"