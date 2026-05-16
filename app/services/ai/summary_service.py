# =========================================================
# FILE: app/services/ai/summary_service.py
# =========================================================

from app.services.ai.brain_service import (
    BrainService
)

from app.services.ai.extraction_service import (
    ExtractionService
)


class SummaryService:

    @staticmethod
    def generate_summary(text):

        if not text:

            return "Không có dữ liệu"

        analysis = (
            BrainService.semantic_document_analysis(
                text
            )
        )

        title = ExtractionService.extract_title(
            text
        )

        issuer = ExtractionService.extract_issuer(
            text
        )

        issue_date = (
            ExtractionService.extract_issue_date(
                text
            )
        )

        summary_core = analysis["summary"]

        final_summary = f"""
Văn bản: {title}

Đơn vị ban hành: {issuer}

Ngày ban hành: {issue_date}

Nội dung chính:
{summary_core}
"""

        return final_summary.strip()