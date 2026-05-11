# =========================================================
# FILE: app/models/database.py
# =========================================================

import sqlite3

from flask import g
from flask import current_app


# =========================================================
# GET DB
# =========================================================
def get_db():

    if 'db' not in g:

        g.db = sqlite3.connect(
            current_app.config['DATABASE']
        )

        # row dạng dict
        g.db.row_factory = sqlite3.Row

        # enable foreign key
        g.db.execute(
            "PRAGMA foreign_keys = ON"
        )

    return g.db


# =========================================================
# CLOSE DB
# =========================================================
def close_db(e=None):

    db = g.pop('db', None)

    if db is not None:
        db.close()


# =========================================================
# INIT DATABASE
# =========================================================
def init_database(app):

    with app.app_context():

        db = get_db()

        # =================================================
        # DEPARTMENTS
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS departments (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT UNIQUE NOT NULL,

            description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # =================================================
        # USERS
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

            avatar TEXT,

            department_id INTEGER,

            is_active INTEGER DEFAULT 1,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(department_id)
                REFERENCES departments(id)
        )
        """)

        # =================================================
        # DOCUMENTS
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            content TEXT,

            file_path TEXT,

            original_filename TEXT,

            document_type TEXT,

            ai_category TEXT,

            priority TEXT DEFAULT 'normal',
                   
            category TEXT,

            status TEXT DEFAULT 'pending',

            ai_summary TEXT,

            ocr_text TEXT,

            extracted_data TEXT,

            ai_suggestion TEXT,

            ai_processed INTEGER DEFAULT 0,

            ai_processing_status TEXT
                DEFAULT 'pending',

            reject_reason TEXT,

            created_by INTEGER,

            assigned_to INTEGER,

            approved_by INTEGER,

            approved_at TIMESTAMP,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(created_by)
                REFERENCES users(id),

            FOREIGN KEY(assigned_to)
                REFERENCES users(id),

            FOREIGN KEY(approved_by)
                REFERENCES users(id)
        )
        """)

        # =================================================
        # APPROVAL HISTORY
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS approval_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            document_id INTEGER,

            action TEXT,

            note TEXT,

            processed_by INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(document_id)
                REFERENCES documents(id)
                ON DELETE CASCADE,

            FOREIGN KEY(processed_by)
                REFERENCES users(id)
        )
        """)

        # =================================================
        # EXTRACTION DATA
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS extraction_data (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            document_id INTEGER,

            field_name TEXT,

            field_value TEXT,

            confidence_score REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(document_id)
                REFERENCES documents(id)
                ON DELETE CASCADE
        )
        """)

        # =================================================
        # AUDIT LOGS
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            action TEXT NOT NULL,

            target_type TEXT,

            target_id INTEGER,

            description TEXT,

            ip_address TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
        """)

        # =================================================
        # NOTIFICATIONS
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS notifications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            title TEXT,

            message TEXT,

            is_read INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """)

        # =================================================
        # DOCUMENT COMMENTS
        # =================================================
        db.execute("""
        CREATE TABLE IF NOT EXISTS document_comments (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            document_id INTEGER,

            user_id INTEGER,

            comment TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(document_id)
                REFERENCES documents(id)
                ON DELETE CASCADE,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
        )
        """)

        # =================================================
        # INDEXES
        # =================================================
        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_status
        ON documents(status)
        """)

        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_title
        ON documents(title)
        """)

        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_created_at
        ON documents(created_at)
        """)

        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_audit_logs_user
        ON audit_logs(user_id)
        """)

        db.commit()

    app.teardown_appcontext(close_db)