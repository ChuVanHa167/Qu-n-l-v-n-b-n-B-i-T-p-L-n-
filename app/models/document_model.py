# =========================================================
# FILE: app/models/document_model.py
# =========================================================

from app.models.database import get_db


class DocumentModel:

    # =====================================================
    # GET DOCUMENT FULL DETAIL
    # =====================================================
    @staticmethod
    def get_document_full_detail(document_id):

        db = get_db()

        return db.execute("""
            SELECT
                documents.*,

                creator.username
                as creator_name,

                assignee.username
                as assignee_name

            FROM documents

            LEFT JOIN users creator
            ON documents.created_by = creator.id

            LEFT JOIN users assignee
            ON documents.assigned_to = assignee.id

            WHERE documents.id = ?
            AND documents.is_deleted = 0
        """, (document_id,)).fetchone()

    @staticmethod
    def get_document_comments(document_id):

        db = get_db()

        return db.execute("""
            SELECT
                document_comments.*,
                users.username
            FROM document_comments

            LEFT JOIN users
            ON document_comments.user_id = users.id

            WHERE document_id = ?

            ORDER BY created_at DESC
        """, (document_id,)).fetchall()

    @staticmethod
    def add_comment(
        document_id,
        user_id,
        comment
    ):

        db = get_db()

        db.execute("""
            INSERT INTO document_comments(
                document_id,
                user_id,
                comment
            )
            VALUES (?, ?, ?)
        """, (
            document_id,
            user_id,
            comment
        ))

        db.commit()

    @staticmethod
    def reject_document(document_id, reason):

        db = get_db()

        db.execute("""
            UPDATE documents
            SET
                status = 'rejected',
                reject_reason = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            reason,
            document_id
        ))

        db.commit()

    @staticmethod
    def get_approval_history(document_id):

        db = get_db()

        return db.execute("""
            SELECT
                approval_history.*,
                users.username
            FROM approval_history

            LEFT JOIN users
            ON approval_history.processed_by = users.id

            WHERE document_id = ?

            ORDER BY created_at DESC
        """, (document_id,)).fetchall()

    @staticmethod
    def create_approval_history(
        document_id,
        action,
        note,
        processed_by
    ):

        db = get_db()

        db.execute("""
            INSERT INTO approval_history(
                document_id,
                action,
                note,
                processed_by
            )
            VALUES (?, ?, ?, ?)
        """, (
            document_id,
            action,
            note,
            processed_by
        ))

        db.commit()

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
            AND is_deleted = 0
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
            WHERE is_deleted = 0
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()


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

            WHERE documents.is_deleted = 0

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
            AND is_deleted = 0
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
            AND is_deleted = 0
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
            AND is_deleted = 0
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
            WHERE is_deleted = 0
            AND (
                title LIKE ?
                OR content LIKE ?
                OR ai_summary LIKE ?
            )
        """, (
            f'%{keyword}%',
            f'%{keyword}%',
            f'%{keyword}%'
        )).fetchall()


    # =====================================================
    # GET STAFF PENDING DOCUMENTS
    # =====================================================
    @staticmethod
    def get_staff_pending_documents(user_id):

        db = get_db()

        return db.execute("""
            SELECT
                documents.*,
                users.username as creator_name
            FROM documents

            LEFT JOIN users
            ON documents.created_by = users.id

            WHERE
                documents.assigned_to = ?
                AND documents.status = 'pending'
                AND documents.is_deleted = 0

            ORDER BY documents.created_at DESC
        """, (user_id,)).fetchall()

    # =====================================================
    # CREATE DOCUMENT
    # =====================================================
    @staticmethod
    def create_document(

        title,
        content,
        document_type,
        created_by,

        category='',

        file_path='',

        original_filename='',

        file_extension='',

        file_size=0,

        priority='normal',

        document_number='',

        issuer='',

        signer='',

        issue_date='',

        keywords='',

        tags='',

        ai_summary='',

        ocr_text='',

        ai_category='',

        ai_confidence=0
    ):

        db = get_db()

        db.execute("""
            INSERT INTO documents (

                title,
                content,
                document_type,
                created_by,

                category,

                file_path,
                original_filename,
                file_extension,
                file_size,

                priority,

                document_number,
                issuer,
                signer,
                issue_date,

                keywords,
                tags,

                ai_summary,
                ocr_text,
                ai_category,

                ai_confidence,

                ai_processed

            )
            VALUES (

                ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, 1
            )
        """, (

            title,
            content,
            document_type,
            created_by,

            category,

            file_path,
            original_filename,
            file_extension,
            file_size,

            priority,

            document_number,
            issuer,
            signer,
            issue_date,

            keywords,
            tags,

            ai_summary,
            ocr_text,
            ai_category,

            ai_confidence
        ))

        db.commit()

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
    def delete_document(
        document_id,
        deleted_by
    ):

        db = get_db()

        db.execute("""
            UPDATE documents
            SET
                is_deleted = 1,
                deleted_at = CURRENT_TIMESTAMP,
                deleted_by = ?
            WHERE id = ?
        """, (
            deleted_by,
            document_id
        ))

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
            WHERE is_deleted = 0
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
            AND is_deleted = 0
        """, (status,)).fetchone()

        return result['total']
    
    # =====================================================
    # FILTER DOCUMENTS
    # =====================================================
    @staticmethod
    def filter_documents(
        keyword='',
        status='',
        document_type=''
    ):

        db = get_db()

        query = """
            SELECT *
            FROM documents
            WHERE is_deleted = 0
        """

        params = []

        if keyword:

            query += """
                AND (
                    title LIKE ?
                    OR content LIKE ?
                )
            """

            params.append(f'%{keyword}%')
            params.append(f'%{keyword}%')

        if status:

            query += """
                AND status = ?
            """

            params.append(status)

        if document_type:

            query += """
                AND document_type = ?
            """

            params.append(document_type)

        query += """
            ORDER BY created_at DESC
        """

        return db.execute(
            query,
            tuple(params)
        ).fetchall()
    
    # =====================================================
    # UPDATE DOCUMENT
    # =====================================================
    @staticmethod
    def update_document(
        document_id,
        title,
        content,
        document_type,
        category,
        priority
    ):

        db = get_db()
        # lưu version cũ
        DocumentModel.save_document_version(
            document_id,
            updated_by=1
        )
        db.execute("""
            UPDATE documents
            SET
                title = ?,
                content = ?,
                document_type = ?,
                category = ?,
                priority = ?,
                version = version + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            title,
            content,
            document_type,
            category,
            priority,
            document_id
        ))

        db.commit()

    # =====================================================
    # SAVE AI PROCESSING RESULT
    # =====================================================
    @staticmethod
    def save_ai_processing_result(
        document_id,
        ocr_text,
        ai_summary,
        ai_category
    ):

        db = get_db()

        db.execute("""
            UPDATE documents
            SET
                ocr_text = ?,
                ai_summary = ?,
                ai_category = ?,
                ai_processed = 1,
                ai_processing_status = 'completed',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            ocr_text,
            ai_summary,
            ai_category,
            document_id
        ))

        db.commit()

    # =====================================================
    # GET STAFF PROCESSING DOCUMENTS
    # =====================================================
    @staticmethod
    def get_staff_processing_documents(user_id):

        db = get_db()

        return db.execute("""
            SELECT
                documents.*,
                users.username as creator_name
            FROM documents

            LEFT JOIN users
            ON documents.created_by = users.id

            WHERE
                documents.assigned_to = ?
                AND documents.status = 'processing'
                AND documents.is_deleted = 0
            ORDER BY documents.updated_at DESC
        """, (user_id,)).fetchall()

    # =====================================================
    # GET STAFF APPROVED DOCUMENTS
    # =====================================================
    @staticmethod
    def get_staff_approved_documents(user_id):

        db = get_db()

        return db.execute("""
            SELECT
                documents.*,
                users.username as creator_name
            FROM documents

            LEFT JOIN users
            ON documents.created_by = users.id

            WHERE
                documents.assigned_to = ?
                AND documents.status = 'approved'
                AND documents.is_deleted = 0
            ORDER BY documents.updated_at DESC
        """, (user_id,)).fetchall()

    # =====================================================
    # STAFF TAKE DOCUMENT
    # =====================================================
    @staticmethod
    def staff_take_document(
        document_id,
        staff_id
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
            staff_id,
            document_id
        ))

        db.commit()

    # =====================================================
    # STAFF COMPLETE DOCUMENT
    # =====================================================
    @staticmethod
    def staff_complete_document(document_id):

        db = get_db()

        db.execute("""
            UPDATE documents
            SET
                status = 'approved',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (document_id,))

        db.commit()

    # =====================================================
    # RESTORE DOCUMENT
    # =====================================================
    @staticmethod
    def restore_document(document_id):

        db = get_db()

        db.execute("""
            UPDATE documents
            SET
                is_deleted = 0,
                deleted_at = NULL,
                deleted_by = NULL
            WHERE id = ?
        """, (document_id,))

        db.commit()

    # =====================================================
    # GET RECYCLE BIN
    # =====================================================
    @staticmethod
    def get_deleted_documents():

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents
            WHERE is_deleted = 1
            ORDER BY deleted_at DESC
        """).fetchall()
    
    # =====================================================
    # SAVE VERSION
    # =====================================================
    @staticmethod
    def save_document_version(
        document_id,
        updated_by
    ):

        db = get_db()

        document = db.execute("""
            SELECT *
            FROM documents
            WHERE id = ?
        """, (document_id,)).fetchone()

        if not document:
            return

        db.execute("""
            INSERT INTO document_versions (

                document_id,
                version_number,

                title,
                content,
                document_type,
                category,
                priority,

                updated_by

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            document['id'],
            document['version'],

            document['title'],
            document['content'],
            document['document_type'],
            document['category'],
            document['priority'],

            updated_by
        ))

        db.commit()

    # =====================================================
    # GET VERSION HISTORY
    # =====================================================
    @staticmethod
    def get_document_versions(document_id):

        db = get_db()

        return db.execute("""
            SELECT
                document_versions.*,
                users.username
            FROM document_versions

            LEFT JOIN users
            ON document_versions.updated_by = users.id

            WHERE document_id = ?

            ORDER BY version_number DESC
        """, (document_id,)).fetchall()
    
    # =====================================================
    # GET OVERDUE DOCUMENTS
    # =====================================================
    @staticmethod
    def get_overdue_documents():

        db = get_db()

        return db.execute("""
            SELECT *
            FROM documents

            WHERE
                deadline IS NOT NULL
                AND deadline < DATE('now')
                AND status != 'approved'
                AND is_deleted = 0
        """).fetchall()