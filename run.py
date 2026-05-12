from app import create_app
from app.context_processors import (
    inject_notifications
)

# =========================
# IMPORT CONFIG
# =========================
from config.development_config import DevelopmentConfig


# =========================
# CREATE APP
# =========================
app = create_app(DevelopmentConfig)
app.context_processor(
    inject_notifications
)

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )