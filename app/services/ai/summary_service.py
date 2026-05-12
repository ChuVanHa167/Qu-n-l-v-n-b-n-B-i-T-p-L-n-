# =========================================================
# FILE: app/services/ai/summary_service.py
# =========================================================

from app.services.ai.brain_service import (
    BrainService
)


class SummaryService:

    @staticmethod
    def generate_summary(text):

        if not text:

            return "Không có dữ liệu"

        return BrainService.intelligent_summary(
            text
        )