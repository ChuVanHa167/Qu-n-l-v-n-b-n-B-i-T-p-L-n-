from app import create_app

# =========================
# IMPORT CONFIG
# =========================
from config.development_config import DevelopmentConfig


# =========================
# CREATE APP
# =========================
app = create_app(DevelopmentConfig)


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )