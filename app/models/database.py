# =========================================================
# FILE: app/models/database.py
# =========================================================
# MỤC ĐÍCH:
# - Quản lý kết nối SQLite
# - Khởi tạo database
# - Tạo bảng dữ liệu
# - Đóng kết nối tự động
#
# DESIGN:
# - Single Responsibility Principle:
#   File này CHỈ chịu trách nhiệm DB
#
# - Open/Closed Principle:
#   Có thể thêm bảng mới mà không sửa logic cũ
#
# - MVC:
#   Đây là tầng MODEL - DATABASE CORE
# =========================================================

import sqlite3
from flask import g, current_app


# =========================================================
# GET DATABASE CONNECTION
# =========================================================
def get_db():
    """
    Lấy kết nối database hiện tại.

    Nếu chưa có kết nối:
    -> tạo mới
    -> lưu vào flask.g

    Flask.g:
    - vùng nhớ request hiện tại
    - mỗi request có 1 connection riêng
    """

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE']
        )

        # Cho phép truy cập row kiểu dict
        # row['username']
        g.db.row_factory = sqlite3.Row

    return g.db


# =========================================================
# CLOSE DATABASE CONNECTION
# =========================================================
def close_db(e=None):
    """
    Đóng kết nối DB sau mỗi request.
    """

    db = g.pop('db', None)

    if db is not None:
        db.close()


# =========================================================
# CREATE ALL TABLES
# =========================================================
def init_database(app):

    with app.app_context():

        db = get_db()

        # =================================================
        # USERS TABLE
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,

            role TEXT NOT NULL,

            full_name TEXT,
            email TEXT,
            phone TEXT,

            is_active INTEGER DEFAULT 1,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # =================================================
        # DOCUMENTS TABLE
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,
            content TEXT,

            document_type TEXT,

            status TEXT DEFAULT 'pending',

            created_by INTEGER,
            assigned_to INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(created_by)
                REFERENCES users(id),

            FOREIGN KEY(assigned_to)
                REFERENCES users(id)
        )
        """)

        # =================================================
        # AUDIT LOGS TABLE
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            action TEXT NOT NULL,

            target_type TEXT,
            target_id INTEGER,

            description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
        """)

        db.commit()

    # tự động đóng db
    app.teardown_appcontext(close_db)