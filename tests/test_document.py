# =========================================================
# FILE: tests/test_documents.py
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
# LOGIN ADMIN HELPER
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
# PREPARE TEST DATA
# =========================================================
def prepare_data(app):

    with app.app_context():

        if not UserModel.user_exists("admin"):

            UserModel.create_user(
                username="admin",
                password="123456",
                role="admin"
            )


# =========================================================
# TEST DOCUMENT PAGE REDIRECT
# =========================================================
def test_document_page_redirect():

    app = create_test_app()

    client = app.test_client()

    response = client.get("/admin/documents")

    # chưa login -> redirect
    assert response.status_code == 302


# =========================================================
# TEST ADMIN DOCUMENT PAGE
# =========================================================
def test_admin_document_page():

    app = create_test_app()

    prepare_data(app)

    client = app.test_client()

    login_admin(client)

    response = client.get("/admin/documents")

    assert response.status_code == 200


# =========================================================
# TEST CREATE DOCUMENT
# =========================================================
def test_create_document():

    app = create_test_app()

    prepare_data(app)

    client = app.test_client()

    login_admin(client)

    response = client.post(
        "/admin/documents/create",
        data={
            "title": "Test Document",
            "content": "Test Content",
            "document_type": "incoming"
        }
    )

    # create xong redirect
    assert response.status_code == 302