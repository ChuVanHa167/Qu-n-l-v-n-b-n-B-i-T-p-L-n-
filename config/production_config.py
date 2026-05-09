# =========================================================
# FILE: config/production_config.py
# =========================================================

"""
=========================================================
PRODUCTION CONFIG
=========================================================

Môi trường production thực tế.

Dùng khi:
- Deploy server
- Chạy thật

ĐẶC ĐIỂM:
- Tắt debug
- Bảo mật cao
- Tối ưu performance
=========================================================
"""

import os


class ProductionConfig:

    # =====================================================
    # BASE DIRECTORY
    # =====================================================
    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    PROJECT_ROOT = os.path.abspath(
        os.path.join(BASE_DIR, "..")
    )

    # =====================================================
    # FLASK CORE
    # =====================================================
    DEBUG = False

    TESTING = False

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "production_secret_key"
    )

    JSON_AS_ASCII = False

    TEMPLATES_AUTO_RELOAD = False

    # =====================================================
    # DATABASE
    # =====================================================
    DATABASE = os.path.join(
        PROJECT_ROOT,
        "database",
        "production.db"
    )

    # =====================================================
    # SESSION
    # =====================================================
    SESSION_PERMANENT = True

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = True

    PERMANENT_SESSION_LIFETIME = 7200

    # =====================================================
    # SECURITY
    # =====================================================
    WTF_CSRF_ENABLED = True

    # =====================================================
    # APPLICATION INFO
    # =====================================================
    APP_NAME = "Smart Document Management System"

    APP_VERSION = "1.0 Production"

    COMPANY_NAME = "Python Project Team"

    # =====================================================
    # PAGINATION
    # =====================================================
    USERS_PER_PAGE = 20

    DOCUMENTS_PER_PAGE = 20

    LOGS_PER_PAGE = 50

    # =====================================================
    # FILE UPLOAD
    # =====================================================
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024

    UPLOAD_FOLDER = os.path.join(
        PROJECT_ROOT,
        "app",
        "static",
        "uploads"
    )

    ALLOWED_EXTENSIONS = {
        'pdf',
        'doc',
        'docx',
        'xls',
        'xlsx',
        'png',
        'jpg',
        'jpeg'
    }

    # =====================================================
    # LOGGING
    # =====================================================
    LOG_LEVEL = "ERROR"

    # =====================================================
    # CACHE
    # =====================================================
    SEND_FILE_MAX_AGE_DEFAULT = 3600