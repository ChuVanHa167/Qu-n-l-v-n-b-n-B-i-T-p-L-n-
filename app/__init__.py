from flask import Flask

# =========================
# IMPORT DATABASE
# =========================
from app.models.database import init_database


# =========================
# IMPORT CONTROLLERS
# =========================
from app.controllers.auth_controller import auth_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.staff_controller import staff_bp
from app.controllers.employee_controller import employee_bp
from app.controllers.document_controller import document_bp


# =========================
# CREATE APP
# =========================
def create_app(config_object):

    app = Flask(__name__)

    # load config
    app.config.from_object(config_object)

    # init database
    init_database(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(document_bp)

    return app