# =========================================================
# FILE: app/__init__.py
# =========================================================

from flask import Flask

# =========================================================
# IMPORT DATABASE
# =========================================================
from app.models.database import init_database

# =========================================================
# IMPORT ROUTES
# =========================================================
from app.routes import ALL_BLUEPRINTS

# =========================================================
# IMPORT UTILS
# =========================================================
from app.utils.formatters import (
    format_datetime,
    format_role,
    format_status
)

from app.utils.constants import SYSTEM_NAME


# =========================================================
# CREATE APP
# =========================================================
def create_app(config_object):

    app = Flask(__name__)

    # =====================================================
    # LOAD CONFIG
    # =====================================================
    app.config.from_object(config_object)

    # =====================================================
    # INIT DATABASE
    # =====================================================
    init_database(app)

    # =====================================================
    # REGISTER BLUEPRINTS
    # =====================================================
    for blueprint in ALL_BLUEPRINTS:
        app.register_blueprint(blueprint)

    # =====================================================
    # REGISTER JINJA FILTERS
    # =====================================================
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['role'] = format_role
    app.jinja_env.filters['status'] = format_status

    # =====================================================
    # GLOBAL TEMPLATE VARIABLES
    # =====================================================
    @app.context_processor
    def inject_global_variables():

        return {
            "SYSTEM_NAME": SYSTEM_NAME
        }

    # =====================================================
    # HOME TEST ROUTE
    # =====================================================
    @app.route('/health')
    def health_check():

        return {
            "status": "success",
            "message": "System running"
        }

    return app