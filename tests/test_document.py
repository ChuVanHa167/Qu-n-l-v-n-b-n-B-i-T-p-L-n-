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
# TEST ADMIN DOCUMENT PAGE
# =========================
def test_document_page_redirect():

    app = create_test_app()

    client = app.test_client()

    response = client.get("/admin/documents")

    # chưa login -> redirect
    assert response.status_code == 302


# =========================
# TEST CREATE DOCUMENT
# =========================
def test_create_document_redirect():

    app = create_test_app()

    client = app.test_client()

    response = client.post(
        "/documents/create",
        data={
            "title": "Test Document",
            "content": "Test Content"
        }
    )

    assert response.status_code == 302