# =========================================================
# FILE: app/services/ai/document_ai_service.py
# =========================================================

from app.services.ai.ocr_service import OCRService

from app.services.ai.summary_service import (
    SummaryService
)

from app.services.ai.extraction_service import (
    ExtractionService
)

from app.services.ai.brain_service import (
    BrainService
)


class DocumentAIService:

    @classmethod
    def process_document(
        cls,
        file_path
    ):

        # =============================================
        # OCR FULL TEXT
        # =============================================
        ocr_text = OCRService.extract_text(
            file_path
        )

        cleaned_text = (
            ExtractionService.clean_content(
                ocr_text
            )
        )

        # =============================================
        # AI SEMANTIC ANALYSIS
        # =============================================
        semantic = (
            BrainService.semantic_document_analysis(
                cleaned_text
            )
        )

        # =============================================
        # SUMMARY
        # =============================================
        summary = SummaryService.generate_summary(
            cleaned_text
        )

        # =============================================
        # EXTRACTION
        # =============================================
        title = ExtractionService.extract_title(
            cleaned_text
        )

        document_type = (
            ExtractionService.extract_document_type(
                cleaned_text
            )
        )

        priority = (
            ExtractionService.extract_priority(
                cleaned_text
            )
        )

        category = (
            ExtractionService.extract_category(
                cleaned_text
            )
        )

        document_number = (
            ExtractionService.extract_document_number(
                cleaned_text
            )
        )

        issue_date = (
            ExtractionService.extract_issue_date(
                cleaned_text
            )
        )

        signer = (
            ExtractionService.extract_signer(
                cleaned_text
            )
        )

        issuer = (
            ExtractionService.extract_issuer(
                cleaned_text
            )
        )

        keywords = (
            ExtractionService.extract_keywords(
                cleaned_text
            )
        )

        return {

            "ocr_text": cleaned_text,

            "summary": summary,

            "title": title,

            "document_type": document_type,

            "priority": priority,

            "category": category,

            "document_number": document_number,

            "issue_date": issue_date,

            "signer": signer,

            "issuer": issuer,

            "keywords": keywords,

            "sentences": semantic["sentences"]
        }