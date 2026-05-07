from app import create_app
from config.testing_config import TestingConfig


# =========================
# CREATE TEST APP
# =========================
def create_test_app():

    app = create_app(TestingConfig)

    app.config["TESTING"] = True

    return app


# =========================
# TEST LOGIN PAGE
# =========================
def test_login_page():

    app = create_test_app()

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


# =========================
# TEST REGISTER PAGE
# =========================
def test_register_page():

    app = create_test_app()

    client = app.test_client()

    response = client.get("/register")

    assert response.status_code == 200


# =========================
# TEST INVALID LOGIN
# =========================
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