# =========================================================
# FILE: config/testing_config.py
# =========================================================

"""
=========================================================
TESTING CONFIG
=========================================================

Môi trường test tự động.

Dùng khi:
- Unit test
- Integration test
- CI/CD

ĐẶC ĐIỂM:
- Database riêng
- TESTING bật
- Không ảnh hưởng dữ liệu thật
=========================================================
"""

import os


class TestingConfig:

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

    TESTING = True

    SECRET_KEY = "testing_secret_key"

    JSON_AS_ASCII = False

    # =====================================================
    # DATABASE
    # =====================================================
    DATABASE = os.path.join(
        PROJECT_ROOT,
        "database",
        "testing.db"
    )

    # =====================================================
    # SESSION
    # =====================================================
    SESSION_PERMANENT = False

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False

    # =====================================================
    # SECURITY
    # =====================================================
    WTF_CSRF_ENABLED = False

    # =====================================================
    # APPLICATION INFO
    # =====================================================
    APP_NAME = "Smart Document Management System"

    APP_VERSION = "1.0 Testing"

    # =====================================================
    # PAGINATION
    # =====================================================
    USERS_PER_PAGE = 5

    DOCUMENTS_PER_PAGE = 5

    LOGS_PER_PAGE = 10

    # =====================================================
    # FILE UPLOAD
    # =====================================================
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    UPLOAD_FOLDER = os.path.join(
        PROJECT_ROOT,
        "tests",
        "uploads"
    )

    # =====================================================
    # LOGGING
    # =====================================================
    LOG_LEVEL = "CRITICAL"