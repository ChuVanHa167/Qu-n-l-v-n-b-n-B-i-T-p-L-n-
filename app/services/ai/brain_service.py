# =========================================================
# FILE: app/services/ai/brain_service.py
# =========================================================

import re
from collections import Counter


class BrainService:

    # =====================================================
    # TOKENIZE
    # =====================================================
    @staticmethod
    def tokenize(text):

        if not text:
            return []

        text = text.lower()

        # bỏ ký tự đặc biệt
        text = re.sub(r'[^\w\s]', ' ', text)

        words = text.split()

        # stop words cơ bản
        stop_words = {

            'và',
            'của',
            'là',
            'có',
            'trong',
            'theo',
            'được',
            'cho',
            'văn',
            'bản',
            'về',
            'các',
            'này',
            'đến',
            'khi',
            'với',
            'để',
            'tại',
            'ngày',
            'tháng',
            'năm'
        }

        return [

            word

            for word in words

            if (
                len(word) > 2
                and
                word not in stop_words
            )
        ]

    # =====================================================
    # KEYWORD SCORE
    # =====================================================
    @classmethod
    def keyword_frequency(
        cls,
        text
    ):

        words = cls.tokenize(text)

        counter = Counter(words)

        return counter.most_common(20)

    # =====================================================
    # SENTENCE SCORE
    # =====================================================
    @classmethod
    def sentence_score(
        cls,
        sentence,
        keywords
    ):

        score = 0

        sentence_lower = sentence.lower()

        for keyword, freq in keywords:

            if keyword in sentence_lower:

                score += freq

        return score

    # =====================================================
    # AI SUMMARY
    # =====================================================
    @classmethod
    def intelligent_summary(
        cls,
        text,
        max_sentences=5
    ):

        if not text:
            return ""

        # tách câu
        sentences = re.split(
            r'[.!?]\s+',
            text
        )

        keywords = cls.keyword_frequency(text)

        scored_sentences = []

        for sentence in sentences:

            score = cls.sentence_score(
                sentence,
                keywords
            )

            scored_sentences.append({
                "sentence": sentence,
                "score": score
            })

        # sort theo score
        scored_sentences.sort(
            key=lambda x: x['score'],
            reverse=True
        )

        # lấy top câu
        top_sentences = scored_sentences[
            :max_sentences
        ]

        summary = '. '.join([
            item['sentence']
            for item in top_sentences
        ])

        return summary[:1200]

    # =====================================================
    # CLASSIFY DOCUMENT
    # =====================================================
    @staticmethod
    def classify_document(text):

        if not text:
            return "Nội bộ"

        text = text.lower()

        rules = {

            "Nhân sự": [
                'nhân sự',
                'tuyển dụng',
                'lao động',
                'cán bộ',
                'nhân viên'
            ],

            "Tài chính": [
                'tài chính',
                'kinh phí',
                'ngân sách',
                'chi tiêu',
                'thuế',
                'lương'
            ],

            "Đào tạo": [
                'đào tạo',
                'sinh viên',
                'học phí',
                'khóa học',
                'giảng viên'
            ],

            "Hành chính": [
                'quyết định',
                'công văn',
                'thông báo',
                'kế hoạch'
            ]
        }

        scores = {}

        for category, keywords in rules.items():

            score = 0

            for keyword in keywords:

                if keyword in text:

                    score += 1

            scores[category] = score

        best_category = max(
            scores,
            key=scores.get
        )

        if scores[best_category] == 0:

            return "Nội bộ"

        return best_category