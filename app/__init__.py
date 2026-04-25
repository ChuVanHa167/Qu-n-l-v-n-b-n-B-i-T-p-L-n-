from flask import Flask
from config import Config
from app.models.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    return app