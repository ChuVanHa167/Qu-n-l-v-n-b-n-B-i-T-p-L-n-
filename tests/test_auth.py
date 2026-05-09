# =========================================================
# FILE: tests/test_auth.py
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
# TEST LOGIN PAGE
# =========================================================
def test_login_page():

    app = create_test_app()

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


# =========================================================
# TEST REGISTER PAGE
# =========================================================
def test_register_page():

    app = create_test_app()

    client = app.test_client()

    response = client.get("/register")

    assert response.status_code == 200


# =========================================================
# TEST INVALID LOGIN
# =========================================================
def test_invalid_login():

    app = create_test_app()

    client = app.test_client()

    response = client.post(
        "/",
        data={
            "username": "wrong",
            "password": "wrong"
        }
    )

    assert response.status_code == 200

    assert b"Sai" in response.data


# =========================================================
# TEST REGISTER USER
# =========================================================
def test_register_user():

    app = create_test_app()

    client = app.test_client()

    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "123456",
            "role": "employee"
        },
        follow_redirects=True
    )

    assert response.status_code == 200


# =========================================================
# TEST VALID LOGIN
# =========================================================
def test_valid_login():

    app = create_test_app()

    with app.app_context():

        if not UserModel.user_exists("admin"):

            UserModel.create_user(
                username="admin",
                password="123456",
                role="admin"
            )

    client = app.test_client()

    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "123456"
        }
    )

    # login thành công -> redirect
    assert response.status_code == 302