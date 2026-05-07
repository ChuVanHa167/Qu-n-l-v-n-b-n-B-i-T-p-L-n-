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
# TEST ADMIN USER PAGE
# =========================
def test_user_page_redirect():

    app = create_test_app()

    client = app.test_client()

    response = client.get("/admin/users")

    # chưa login -> redirect
    assert response.status_code == 302


# =========================
# TEST CREATE USER
# =========================
def test_create_user_redirect():

    app = create_test_app()

    client = app.test_client()

    response = client.post(
        "/admin/users/create",
        data={
            "username": "testuser",
            "password": "123456",
            "role": "employee"
        }
    )

    assert response.status_code == 302