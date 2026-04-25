import sqlite3
from flask import g

DATABASE = "database.db"

def get_db():
    # nếu chưa có connection thì tạo mới
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, check_same_thread=False)

        # trả về dạng dict thay vì tuple
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    # đóng kết nối khi request kết thúc
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # tạo bảng users nếu chưa có
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
        """)

        db.commit()

    # auto đóng db sau mỗi request
    app.teardown_appcontext(close_db)