from app.models.db import get_db

class UserModel:

    @staticmethod
    def find_by_username(username):
        db = get_db()

        return db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    @staticmethod
    def create_user(username, password, role):
        db = get_db()

        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )

        db.commit()

    @staticmethod
    def user_exists(username):
        return UserModel.find_by_username(username) is not None