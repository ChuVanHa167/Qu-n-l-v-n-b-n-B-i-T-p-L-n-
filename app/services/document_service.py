# =========================================================
# FILE: app/services/document_service.py
# =========================================================
# MỤC ĐÍCH:
# - Business logic cho Documents
#
# CHỨC NĂNG:
# - CRUD document
# - Assign document
# - Approve / Reject
# - Dashboard statistics
#
# SOLID:
# - Chỉ xử lý logic nghiệp vụ document
# =========================================================

from app.models.document_model import DocumentModel


class DocumentService:

    # =====================================================
    # GET ALL DOCUMENTS
    # =====================================================
    @staticmethod
    def get_all_documents():

        return DocumentModel.get_all_documents()

    # =====================================================
    # GET DOCUMENT BY ID
    # =====================================================
    @staticmethod
    def get_document_by_id(document_id):

        document = DocumentModel.get_document_by_id(
            document_id
        )

        if not document:

            return {
                'success': False,
                'message': 'Không tìm thấy văn bản!'
            }

        return {
            'success': True,
            'document': document
        }

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
        priority='normal',
        file_path='',
        original_filename=''
    ):

        # validate
        if not title:

            return {
                'success': False,
                'message': 'Tiêu đề không được để trống!'
            }

        # tạo document
        DocumentModel.create_document(
            title=title,
            content=content,
            document_type=document_type,
            created_by=created_by,
            category=category,
            priority=priority,
            file_path=file_path,
            original_filename=original_filename
        )

        return {
            'success': True,
            'message': 'Tạo văn bản thành công!'
        }

    # =====================================================
    # UPDATE STATUS
    # =====================================================
    @staticmethod
    def update_document_status(
        document_id,
        status,
        reject_reason=''
    ):

        valid_status = [
            'pending',
            'processing',
            'approved',
            'rejected',
            'completed'
        ]

        # validate status
        if status not in valid_status:

            return {
                'success': False,
                'message': 'Trạng thái không hợp lệ!'
            }

        DocumentModel.update_document_status(
            document_id=document_id,
            status=status,
            reject_reason=reject_reason
        )

        return {
            'success': True,
            'message': 'Cập nhật trạng thái thành công!'
        }

    # =====================================================
    # ASSIGN DOCUMENT
    # =====================================================
    @staticmethod
    def assign_document(
        document_id,
        assigned_to
    ):

        DocumentModel.assign_document(
            document_id,
            assigned_to
        )

        return {
            'success': True,
            'message': 'Phân công văn bản thành công!'
        }

    # =====================================================
    # APPROVE DOCUMENT
    # =====================================================
    @staticmethod
    def approve_document(
        document_id,
        approved_by
    ):

        DocumentModel.approve_document(
            document_id,
            approved_by
        )

        return {
            'success': True,
            'message': 'Duyệt văn bản thành công!'
        }

    # =====================================================
    # REJECT DOCUMENT
    # =====================================================
    @staticmethod
    def reject_document(
        document_id,
        reject_reason=''
    ):

        DocumentModel.reject_document(
            document_id,
            reject_reason
        )

        return {
            'success': True,
            'message': 'Đã từ chối văn bản!'
        }

    # =====================================================
    # DELETE DOCUMENT
    # =====================================================
    @staticmethod
    def delete_document(document_id):

        document = DocumentModel.get_document_by_id(
            document_id
        )

        if not document:

            return {
                'success': False,
                'message': 'Văn bản không tồn tại!'
            }

        DocumentModel.delete_document(document_id)

        return {
            'success': True,
            'message': 'Xóa văn bản thành công!'
        }

    # =====================================================
    # SEARCH DOCUMENTS
    # =====================================================
    @staticmethod
    def search_documents(keyword):

        if not keyword:

            return []

        return DocumentModel.search_documents(keyword)

    # =====================================================
    # GET DOCUMENTS BY STATUS
    # =====================================================
    @staticmethod
    def get_documents_by_status(status):

        return DocumentModel.get_documents_by_status(
            status
        )

    # =====================================================
    # GET DOCUMENTS BY USER
    # =====================================================
    @staticmethod
    def get_documents_by_user(user_id):

        return DocumentModel.get_documents_by_user(
            user_id
        )

    # =====================================================
    # GET ASSIGNED DOCUMENTS
    # =====================================================
    @staticmethod
    def get_assigned_documents(user_id):

        return DocumentModel.get_assigned_documents(
            user_id
        )

    # =====================================================
    # DASHBOARD STATISTICS
    # =====================================================
    @staticmethod
    def count_documents():

        return DocumentModel.count_documents()

    @staticmethod
    def count_pending_documents():

        return DocumentModel.count_by_status(
            'pending'
        )

    @staticmethod
    def count_processing_documents():

        return DocumentModel.count_by_status(
            'processing'
        )

    @staticmethod
    def count_approved_documents():

        return DocumentModel.count_by_status(
            'approved'
        )

    @staticmethod
    def count_rejected_documents():

        return DocumentModel.count_by_status(
            'rejected'
        )

    @staticmethod
    def count_completed_documents():

        return DocumentModel.count_by_status(
            'completed'
        )