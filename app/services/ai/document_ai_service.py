# =========================================================
# FILE: app/services/ai/document_ai_service.py
# =========================================================

from app.services.ai.ocr_service import OCRService
from app.services.ai.summary_service import SummaryService
from app.services.ai.category_service import CategoryService
from app.services.ai.extraction_service import (
    ExtractionService
)


class DocumentAIService:

    @classmethod
    def process_document(
        cls,
        file_path
    ):

        # OCR
        ocr_text = OCRService.extract_text(
            file_path
        )

        # SUMMARY
        summary = SummaryService.generate_summary(
            ocr_text
        )

        # CATEGORY
        category = CategoryService.detect_category(
            ocr_text
        )

        # TITLE
        title = ExtractionService.extract_title(
            ocr_text
        )

        # DOCUMENT TYPE
        document_type = (
            ExtractionService.extract_document_type(
                ocr_text
            )
        )

        # PRIORITY
        priority = (
            ExtractionService.extract_priority(
                ocr_text
            )
        )

        # EXTRA METADATA
        document_number = (
            ExtractionService.extract_document_number(
                ocr_text
            )
        )

        issue_date = (
            ExtractionService.extract_issue_date(
                ocr_text
            )
        )

        signer = (
            ExtractionService.extract_signer(
                ocr_text
            )
        )

        issuer = (
            ExtractionService.extract_issuer(
                ocr_text
            )
        )

        keywords = (
            ExtractionService.extract_keywords(
                ocr_text
            )
        )

        # CLEAN CONTENT
        content = (
            ExtractionService.clean_content(
                ocr_text
            )
        )

        return {

            "ocr_text": ocr_text,

            "summary": summary,

            "category": category,

            "title": title,

            "document_type": document_type,

            "priority": priority,

            "content": content,

            "document_number":
                ExtractionService.extract_document_number(
                    ocr_text
                ),

            "issue_date":
                ExtractionService.extract_issue_date(
                    ocr_text
                ),

            "signer":
                ExtractionService.extract_signer(
                    ocr_text
                ),

            "issuer":
                ExtractionService.extract_issuer(
                    ocr_text
                ),

            "keywords":
                ExtractionService.extract_keywords(
                    ocr_text
                )
        }