# =========================================================
# FILE: app/models/document_model.py
# =========================================================
# MỤC ĐÍCH:
# - Quản lý dữ liệu văn bản
#
# SOLID:
# - Chỉ xử lý DOCUMENTS
# - Không chứa auth logic
# - Không render template
# =========================================================

from app.models.database import get_db


class DocumentModel:

    # =====================================================
    # CREATE DOCUMENT
    # =====================================================
    @staticmethod
    def create_document(
        title,
        content,
        document_type,
        created_by
    ):

        db = get_db()

        db.execute("""
            INSERT INTO documents (
                title,
                content,
                document_type,
                created_by
            )
            VALUES (?, ?, ?, ?)
        """, (
            title,
            content,
            document_type,
            created_by
        ))

        db.commit()

    # =====================================================
    # GET ALL DOCUMENTS
    # =====================================================
    @staticmethod
    def get_all_documents():

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            ORDER BY created_at DESC
        """).fetchall()

    # =====================================================
    # GET DOCUMENT BY ID
    # =====================================================
    @staticmethod
    def get_document_by_id(document_id):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            WHERE id = ?
        """, (document_id,)).fetchone()

    # =====================================================
    # UPDATE DOCUMENT STATUS
    # =====================================================
    @staticmethod
    def update_document_status(
        document_id,
        status
    ):

        db = get_db()

        db.execute("""
            UPDATE documents
            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            status,
            document_id
        ))

        db.commit()

    # =====================================================
    # ASSIGN DOCUMENT
    # =====================================================
    @staticmethod
    def assign_document(
        document_id,
        assigned_to
    ):

        db = get_db()

        db.execute("""
            UPDATE documents
            SET
                assigned_to = ?,
                status = 'processing',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            assigned_to,
            document_id
        ))

        db.commit()

    # =====================================================
    # DELETE DOCUMENT
    # =====================================================
    @staticmethod
    def delete_document(document_id):

        db = get_db()

        db.execute("""
            DELETE FROM documents
            WHERE id = ?
        """, (document_id,))

        db.commit()

    # =====================================================
    # COUNT DOCUMENTS
    # =====================================================
    @staticmethod
    def count_documents():

        db = get_db()

        result = db.execute("""
            SELECT COUNT(*) as total
            FROM documents
        """).fetchone()

        return result['total']

    # =====================================================
    # COUNT DOCUMENTS BY STATUS
    # =====================================================
    @staticmethod
    def count_by_status(status):

        db = get_db()

        result = db.execute("""
            SELECT COUNT(*) as total
            FROM documents
            WHERE status = ?
        """, (status,)).fetchone()

        return result['total']