# =========================================================
# FILE: config/development_config.py
# =========================================================

"""
=========================================================
DEVELOPMENT CONFIG
=========================================================

Môi trường phát triển local.

Dùng khi:
- Code local
- Debug
- Test giao diện
- Test database

ĐẶC ĐIỂM:
- DEBUG bật
- Auto reload
- Log chi tiết
=========================================================
"""

import os


class DevelopmentConfig:

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
    DEBUG = True

    TESTING = False

    SECRET_KEY = "development_secret_key"

    JSON_AS_ASCII = False

    TEMPLATES_AUTO_RELOAD = True

    # =====================================================
    # DATABASE
    # =====================================================
    DATABASE = os.path.join(
        PROJECT_ROOT,
        "database",
        "development.db"
    )

    # =====================================================
    # SESSION
    # =====================================================
    SESSION_PERMANENT = False

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False

    PERMANENT_SESSION_LIFETIME = 3600

    # =====================================================
    # SECURITY
    # =====================================================
    WTF_CSRF_ENABLED = False

    # =====================================================
    # APPLICATION INFO
    # =====================================================
    APP_NAME = "Smart Document Management System"

    APP_VERSION = "1.0 Development"

    COMPANY_NAME = "Python Project Team"

    # =====================================================
    # PAGINATION
    # =====================================================
    USERS_PER_PAGE = 10

    DOCUMENTS_PER_PAGE = 10

    LOGS_PER_PAGE = 20

    # =====================================================
    # FILE UPLOAD
    # =====================================================
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

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
    LOG_LEVEL = "DEBUG"

    # =====================================================
    # CACHE
    # =====================================================
    SEND_FILE_MAX_AGE_DEFAULT = 0