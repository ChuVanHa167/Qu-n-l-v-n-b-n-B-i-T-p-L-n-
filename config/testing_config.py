# =========================================================
# FILE: config/testing_config.py
# =========================================================

"""
Testing Config
--------------
Môi trường test tự động.

Dùng khi:
- unit test
- integration test
- CI/CD

ĐẶC ĐIỂM:
- database riêng
- TESTING bật
- không ảnh hưởng dữ liệu thật
"""

import os


class TestingConfig:

    # =====================================================
    # FLASK CORE
    # =====================================================
    DEBUG = False

    TESTING = True

    SECRET_KEY = "testing_secret_key"

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
        "testing.db"
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

    APP_VERSION = "1.0 Testing"

    # =====================================================
    # PAGINATION
    # =====================================================
    USERS_PER_PAGE = 5

    DOCUMENTS_PER_PAGE = 5

    # =====================================================
    # FILE UPLOAD
    # =====================================================
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    UPLOAD_FOLDER = "tests/uploads"

    # =====================================================
    # LOGGING
    # =====================================================
    LOG_LEVEL = "CRITICAL"