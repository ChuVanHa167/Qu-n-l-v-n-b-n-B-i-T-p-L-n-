# ============================================
# FILE: app/services/document_service.py
# ============================================

from app.models.document_model import DocumentModel


class DocumentService:
    """
    ==================================
    DOCUMENT SERVICE
    ==================================
    Xử lý business logic văn bản
    """

    @staticmethod
    def get_all_documents():

        return DocumentModel.get_all_documents()

    @staticmethod
    def get_document_by_id(doc_id):

        return DocumentModel.get_document_by_id(doc_id)

    @staticmethod
    def create_document(title, content, doc_type, created_by):

        if not title:
            return {
                'success': False,
                'message': 'Tiêu đề không được để trống!'
            }

        DocumentModel.create_document(
            title,
            content,
            doc_type,
            created_by
        )

        return {
            'success': True,
            'message': 'Tạo văn bản thành công!'
        }

    @staticmethod
    def delete_document(doc_id):

        DocumentModel.delete_document(doc_id)

        return {
            'success': True,
            'message': 'Xóa văn bản thành công!'
        }

    @staticmethod
    def update_document_status(doc_id, status):

        DocumentModel.update_document_status(doc_id, status)

        return {
            'success': True,
            'message': 'Cập nhật trạng thái thành công!'
        }

    @staticmethod
    def assign_document(doc_id, username):

        DocumentModel.assign_document(doc_id, username)

        return {
            'success': True,
            'message': 'Phân công văn bản thành công!'
        }

    # ==================================
    # DASHBOARD
    # ==================================

    @staticmethod
    def count_documents():

        return DocumentModel.count_documents()

    @staticmethod
    def count_pending_documents():

        return DocumentModel.count_by_status('pending')

    @staticmethod
    def count_processing_documents():

        return DocumentModel.count_by_status('processing')

    @staticmethod
    def count_done_documents():

        return DocumentModel.count_by_status('done')