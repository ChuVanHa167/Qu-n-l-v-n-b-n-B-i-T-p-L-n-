# =========================================================
# FILE: app/models/document_model.py
# =========================================================

from app.models.database import get_db


class DocumentModel:

    # =====================================================
    # GET DOCUMENTS BY STATUS
    # =====================================================
    @staticmethod
    def get_documents_by_status(status):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            WHERE status = ?
            ORDER BY created_at DESC
        """, (status,)).fetchall()

    # =====================================================
    # GET DOCUMENTS BY STATUS
    # =====================================================
    @staticmethod
    def get_documents_by_status(status):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            WHERE status = ?
            ORDER BY created_at DESC
        """, (status,)).fetchall()

    # =====================================================
    # GET DOCUMENTS BY ASSIGNEE
    # =====================================================
    @staticmethod
    def get_documents_by_assignee(user_id):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            WHERE assigned_to = ?
            ORDER BY created_at DESC
        """, (user_id,)).fetchall()


    # =====================================================
    # GET RECENT DOCUMENTS
    # =====================================================
    @staticmethod
    def get_recent_documents(limit=5):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()

    # =====================================================
    # CREATE DOCUMENT
    # =====================================================
    @staticmethod
    def create_document(
        title,
        content,
        document_type,
        created_by,
        file_path='',
        priority='normal'
    ):

        db = get_db()

        db.execute("""
            INSERT INTO documents (
                title,
                content,
                document_type,
                created_by,
                file_path,
                priority
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title,
            content,
            document_type,
            created_by,
            file_path,
            priority
        ))

        db.commit()

    # =====================================================
    # GET ALL DOCUMENTS
    # =====================================================
    @staticmethod
    def get_all_documents():

        db = get_db()

        return db.execute("""
            SELECT
                documents.*,
                users.username as creator_name
            FROM documents

            LEFT JOIN users
            ON documents.created_by = users.id

            ORDER BY documents.created_at DESC
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
    # GET DOCUMENTS BY CREATOR
    # =====================================================
    @staticmethod
    def get_documents_by_creator(user_id):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            WHERE created_by = ?
            ORDER BY created_at DESC
        """, (user_id,)).fetchall()

    # =====================================================
    # GET ASSIGNED DOCUMENTS
    # =====================================================
    @staticmethod
    def get_assigned_documents(user_id):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            WHERE assigned_to = ?
            ORDER BY created_at DESC
        """, (user_id,)).fetchall()

    # =====================================================
    # SEARCH DOCUMENTS
    # =====================================================
    @staticmethod
    def search_documents(keyword):

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            WHERE
                title LIKE ?
                OR content LIKE ?
                OR ai_summary LIKE ?
        """, (
            f'%{keyword}%',
            f'%{keyword}%',
            f'%{keyword}%'
        )).fetchall()

    # =====================================================
    # UPDATE STATUS
    # =====================================================
    @staticmethod
    def update_document_status(document_id, status):

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
    # UPDATE AI RESULT
    # =====================================================
    @staticmethod
    def update_ai_result(
        document_id,
        ocr_text,
        ai_category,
        ai_summary
    ):

        db = get_db()

        db.execute("""
            UPDATE documents
            SET
                ocr_text = ?,
                ai_category = ?,
                ai_summary = ?,
                ai_processed = 1
            WHERE id = ?
        """, (
            ocr_text,
            ai_category,
            ai_summary,
            document_id
        ))

        db.commit()

    # =====================================================
    # ASSIGN DOCUMENT
    # =====================================================
    @staticmethod
    def assign_document(document_id, assigned_to):

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
    # COUNT BY STATUS
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
    
