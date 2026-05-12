from app.models.database import get_db


class SettingsModel:

    @staticmethod
    def get_setting(key):

        db = get_db()

        result = db.execute("""
            SELECT setting_value
            FROM settings
            WHERE setting_key = ?
        """, (key,)).fetchone()

        if result:
            return result['setting_value']

        return ''

    @staticmethod
    def set_setting(key, value):

        db = get_db()

        exists = db.execute("""
            SELECT id
            FROM settings
            WHERE setting_key = ?
        """, (key,)).fetchone()

        if exists:

            db.execute("""
                UPDATE settings
                SET setting_value = ?
                WHERE setting_key = ?
            """, (value, key))

        else:

            db.execute("""
                INSERT INTO settings(
                    setting_key,
                    setting_value
                )
                VALUES (?, ?)
            """, (key, value))

        db.commit()