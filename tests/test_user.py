# =========================================================
# FILE: tests/test_users.py
# =========================================================

from app import create_app

from config.testing_config import TestingConfig

from app.models.user_model import UserModel


# =========================================================
# CREATE TEST APP
# =========================================================
def create_test_app():

    app = create_app(TestingConfig)

    app.config["TESTING"] = True

    return app


# =========================================================
# PREPARE ADMIN ACCOUNT
# =========================================================
def prepare_admin(app):

    with app.app_context():

        if not UserModel.user_exists("admin"):

            UserModel.create_user(
                username="admin",
                password="123456",
                role="admin"
            )


# =========================================================
# LOGIN ADMIN
# =========================================================
def login_admin(client):

    return client.post(
        "/",
        data={
            "username": "admin",
            "password": "123456"
        }
    )


# =========================================================
# TEST USER PAGE REDIRECT
# =========================================================
def test_user_page_redirect():

    app = create_test_app()

    client = app.test_client()

    response = client.get("/admin/users")

    # chưa login -> redirect
    assert response.status_code == 302


# =========================================================
# TEST USER PAGE SUCCESS
# =========================================================
def test_user_page_success():

    app = create_test_app()

    prepare_admin(app)

    client = app.test_client()

    login_admin(client)

    response = client.get("/admin/users")

    assert response.status_code == 200


# =========================================================
# TEST CREATE USER
# =========================================================
def test_create_user():

    app = create_test_app()

    prepare_admin(app)

    client = app.test_client()

    login_admin(client)

    response = client.post(
        "/admin/users/create",
        data={
            "username": "testuser",
            "password": "123456",
            "role": "employee"
        }
    )

    assert response.status_code == 302