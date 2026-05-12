# =========================================================
# FILE: app/services/ai/category_service.py
# =========================================================

from app.services.ai.brain_service import (
    BrainService
)


class CategoryService:

    @staticmethod
    def detect_category(text):

        return BrainService.classify_document(
            text
        )