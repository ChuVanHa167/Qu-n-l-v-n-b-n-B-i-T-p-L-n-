
# =========================================================
# FILE: app/services/ai/brain_service.py
# =========================================================

import re

from collections import Counter


class BrainService:

    # =====================================================
    # CLEAN TEXT
    # =====================================================
    @staticmethod
    def normalize_text(text):

        if not text:
            return ""

        text = text.replace('\r', '\n')

        text = re.sub(r'[ \t]+', ' ', text)

        text = re.sub(r'\n{2,}', '\n', text)

        return text.strip()

    # =====================================================
    # SPLIT PARAGRAPHS
    # =====================================================
    @classmethod
    def split_paragraphs(
        cls,
        text
    ):

        text = cls.normalize_text(text)

        paragraphs = []

        for p in text.split('\n'):

            p = p.strip()

            if len(p) > 30:

                paragraphs.append(p)

        return paragraphs

    # =====================================================
    # SPLIT SENTENCES
    # =====================================================
    @staticmethod
    def split_sentences(text):

        if not text:
            return []

        sentences = re.split(
            r'(?<=[\.\!\?])\s+',
            text
        )

        clean_sentences = []

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) > 15:

                clean_sentences.append(
                    sentence
                )

        return clean_sentences

    # =====================================================
    # TOKENIZE
    # =====================================================
    @staticmethod
    def tokenize(text):

        if not text:
            return []

        text = text.lower()

        text = re.sub(
            r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]',
            ' ',
            text
        )

        words = text.split()

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
            'năm',
            'cộng',
            'hòa',
            'xã',
            'hội',
            'chủ',
            'nghĩa',
            'việt',
            'nam'
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

        return counter.most_common(30)

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

        length = len(
            sentence.split()
        )

        if 12 <= length <= 40:

            score += 8

        return score

    # =====================================================
    # AI SUMMARY
    # =====================================================
    @classmethod
    def intelligent_summary(
        cls,
        text,
        max_sentences=6
    ):

        if not text:
            return ""

        text = cls.normalize_text(text)

        sentences = cls.split_sentences(
            text
        )

        keywords = cls.keyword_frequency(
            text
        )

        important_patterns = [

            'quyết định',
            'yêu cầu',
            'đề nghị',
            'thông báo',
            'triển khai',
            'thực hiện',
            'căn cứ',
            'nhằm',
            'giao cho',
            'chịu trách nhiệm',
            'áp dụng',
            'ban hành'
        ]

        scored_sentences = []

        for index, sentence in enumerate(
            sentences
        ):

            score = cls.sentence_score(
                sentence,
                keywords
            )

            lower = sentence.lower()

            # =================================
            # boost semantic
            # =================================
            for pattern in important_patterns:

                if pattern in lower:

                    score += 15

            # =================================
            # ưu tiên đoạn đầu
            # =================================
            if index < 10:

                score += 8

            # =================================
            # câu vừa phải
            # =================================
            word_count = len(
                sentence.split()
            )

            if 15 <= word_count <= 45:

                score += 10

            # =================================
            # loại OCR noise
            # =================================
            if len(sentence) < 20:

                score -= 20

            if sentence.count('.....') > 0:

                score -= 30

            scored_sentences.append({

                "sentence": sentence,

                "score": score,

                "index": index
            })

        scored_sentences.sort(
            key=lambda x: x['score'],
            reverse=True
        )

        top_sentences = scored_sentences[
            :max_sentences
        ]

        top_sentences.sort(
            key=lambda x: x['index']
        )

        final_summary = []

        for item in top_sentences:

            final_summary.append(
                item['sentence']
            )

        return '\n\n'.join(
            final_summary
        )[:2000]


    # =====================================================
    # DOCUMENT SEMANTIC ANALYSIS
    # =====================================================
    @classmethod
    def semantic_document_analysis(
        cls,
        text
    ):

        text = cls.normalize_text(
            text
        )

        paragraphs = cls.split_paragraphs(
            text
        )

        sentences = cls.split_sentences(
            text
        )

        keywords = cls.keyword_frequency(
            text
        )

        summary = cls.intelligent_summary(
            text
        )

        return {

            "paragraphs": paragraphs,

            "sentences": sentences,

            "keywords": keywords,

            "summary": summary
        }

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

                score += text.count(
                    keyword
                )

            scores[category] = score

        best_category = max(
            scores,
            key=scores.get
        )

        if scores[best_category] == 0:

            return "Nội bộ"

        return best_category
