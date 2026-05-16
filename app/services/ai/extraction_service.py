# =========================================================
# FILE: app/services/ai/extraction_service.py
# =========================================================

import re

from app.services.ai.brain_service import (
    BrainService
)



class ExtractionService:

    # =====================================================
    # TITLE
    # =====================================================
    @staticmethod
    def extract_title(text):

        if not text:
            return "Không xác định"

        lines = [

            line.strip()

            for line in text.split('\n')

            if line.strip()
        ]

        document_keywords = [

            'quyết định',
            'thông báo',
            'kế hoạch',
            'báo cáo',
            'công văn',
            'biên bản'
        ]

        ignore_keywords = [

            'cộng hòa',
            'độc lập',
            'tự do',
            'hạnh phúc',
            'số:',
            'ubnd',
            'ngày'
        ]

        for i, line in enumerate(lines[:40]):

            lower = line.lower()

            if any(
                keyword in lower
                for keyword in document_keywords
            ):

                title_parts = []

                for j in range(
                    i + 1,
                    min(i + 5, len(lines))
                ):

                    next_line = lines[j].strip()

                    next_lower = next_line.lower()

                    if any(
                        keyword in next_lower
                        for keyword in ignore_keywords
                    ):
                        continue

                    if len(next_line) > 8:

                        title_parts.append(next_line)

                if title_parts:

                    return ' '.join(title_parts)

        return "Không xác định"


    # =====================================================
    # DOCUMENT NUMBER
    # =====================================================
    @staticmethod
    def extract_document_number(text):

        if not text:
            return ""

        lines = [

            line.strip()

            for line in text.split('\n')

            if line.strip()
        ]

        patterns = [

            r'Số\s*[:\-]?\s*(.+)',

            r'SỐ\s*[:\-]?\s*(.+)',

            r'So\s*[:\-]?\s*(.+)'
        ]

        blacklist = [

            'cộng hòa',
            'độc lập',
            'hạnh phúc'
        ]

        for line in lines[:40]:

            lower = line.lower()

            if any(
                bad in lower
                for bad in blacklist
            ):
                continue

            for pattern in patterns:

                match = re.search(
                    pattern,
                    line,
                    re.IGNORECASE
                )

                if match:

                    value = match.group(1)

                    value = value.strip()

                    value = re.sub(r'\s+', '', value)

                    # remove ký tự rác cuối
                    value = value.strip('.,;:')

                    if len(value) > 2:

                        return value

        return ""

    # =====================================================
    # ISSUE DATE
    # =====================================================
    @staticmethod
    def extract_issue_date(text):

        patterns = [

            r'ngày\s+\d{1,2}\s+tháng\s+\d{1,2}\s+năm\s+\d{4}',

            r'\d{1,2}/\d{1,2}/\d{4}'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group(0)

        return ""


    # =====================================================
    # SIGNER
    # =====================================================
    @staticmethod
    def extract_signer(text):

        if not text:
            return ""

        lines = [

            line.strip()

            for line in text.split('\n')

            if line.strip()
        ]

        signer_roles = [

            'hiệu trưởng',
            'phó hiệu trưởng',
            'trưởng phòng',
            'giám đốc',
            'phó giám đốc',
            'chủ tịch',
            'phó chủ tịch',
            'kt.',
            'tl.',
            'tuq.'
        ]

        invalid_words = [

            'khoa',
            'viện',
            'phòng đào tạo',
            'bộ môn',
            'website',
            'email',
            'điện thoại',
            'nơi nhận',
            'sinh viên'
        ]

        # =========================================
        # CLEAN OCR NAME
        # =========================================
        def clean_ocr_name(name):

            # remove nhiều space
            name = re.sub(r'\s+', ' ', name)

            # fix OCR kiểu:
            # Th ị -> Thị
            name = re.sub(
                r'([A-Za-zÀ-ỹ])\s+([ịỉĩíì])',
                r'\1\2',
                name
            )

            name = re.sub(
                r'([A-Za-zÀ-ỹ])\s+([ưứừửữự])',
                r'\1\2',
                name
            )

            name = re.sub(
                r'([A-Za-zÀ-ỹ])\s+([ờớởỡợ])',
                r'\1\2',
                name
            )

            # bỏ học vị
            name = re.sub(
                r'^(ths\.?|ts\.?|pgs\.?|gs\.?)\s*',
                '',
                name,
                flags=re.IGNORECASE
            )

            return name.strip()

        # =========================================
        # VALID PERSON NAME
        # =========================================
        def is_valid_person_name(name):

            if not name:
                return False

            lower = name.lower()

            if any(
                bad in lower
                for bad in invalid_words
            ):
                return False

            if any(char.isdigit() for char in name):
                return False

            words = name.split()

            if len(words) < 2:
                return False

            if len(words) > 6:
                return False

            return True

        # =========================================
        # SCAN TOÀN BỘ VĂN BẢN
        # =========================================
        for i, line in enumerate(lines):

            lower = line.lower()

            if any(
                role in lower
                for role in signer_roles
            ):

                # lấy block dưới vùng ký
                block = []

                for j in range(
                    i + 1,
                    min(i + 8, len(lines))
                ):

                    block.append(lines[j])

                merged = ' '.join(block)

                merged = clean_ocr_name(
                    merged
                )

                print("\nSIGN BLOCK:")
                print(merged)

                # =====================================
                # tìm tên kiểu:
                # Phan Thị Thu Hường
                # Chử Văn Hà
                # =====================================
                matches = re.findall(

                    r'([A-ZÀ-Ỹ][^\d\,\;\:\(\)]{5,60})',

                    merged
                )

                if matches:

                    # lấy cụm cuối cùng
                    candidate = matches[-1]

                    candidate = clean_ocr_name(
                        candidate
                    )

                    # fix OCR spacing mạnh hơn
                    candidate = re.sub(
                        r'\s+',
                        ' ',
                        candidate
                    )

                    candidate = candidate.replace(
                        ' Th ị ',
                        ' Thị '
                    )

                    candidate = candidate.replace(
                        ' Hư ờng ',
                        ' Hường '
                    )

                    candidate = candidate.strip()

                    if is_valid_person_name(
                        candidate
                    ):

                        return candidate.title()

        return ""

    # =====================================================
    # ISSUER
    # =====================================================
    @staticmethod
    def extract_issuer(text):

        lines = text.split('\n')[:20]

        keywords = [

            'trường',
            'đại học',
            'ubnd',
            'ủy ban',
            'bộ',
            'sở',
            'phòng'
        ]

        for line in lines:

            lower = line.lower()

            if any(
                keyword in lower
                for keyword in keywords
            ):

                return line.strip()

        return ""

    # =====================================================
    # DOCUMENT TYPE
    # =====================================================
    @staticmethod
    def extract_document_type(text):

        text = text.lower()

        mapping = {

            'quyết định': 'decision',
            'kế hoạch': 'plan',
            'thông báo': 'notification',
            'báo cáo': 'report',
            'công văn': 'incoming'
        }

        scores = {}

        first_part = text[:3000]

        for keyword, value in mapping.items():

            count = first_part.count(keyword)

            if count:

                scores[value] = count

        if scores:

            return max(
                scores,
                key=scores.get
            )

        return 'incoming'

    # =====================================================
    # PRIORITY
    # =====================================================
    @staticmethod
    def extract_priority(text):

        text = text.lower()

        if 'hỏa tốc' in text:
            return 'urgent'

        if 'thượng khẩn' in text:
            return 'urgent'

        if 'khẩn' in text:
            return 'high'

        return 'normal'

    # =====================================================
    # CATEGORY
    # =====================================================
    @staticmethod
    def extract_category(text):

        return BrainService.classify_document(
            text
        )

    # =====================================================
    # KEYWORDS
    # =====================================================
    @staticmethod
    def extract_keywords(text):

        sentences = BrainService.split_sentences(
            text
        )

        final_keywords = []

        for sentence in sentences[:25]:

            words = BrainService.tokenize(sentence)

            if len(words) >= 2:

                phrase = ' '.join(words[:2])

                if phrase not in final_keywords:

                    final_keywords.append(
                        phrase
                    )

            if len(final_keywords) >= 5:
                break

        return ', '.join(final_keywords)

    # =====================================================
    # CLEAN CONTENT
    # =====================================================
    @staticmethod
    def clean_content(text):

        if not text:
            return ""

        text = re.sub(r'\n+', '\n', text)

        text = re.sub(r'[ \t]+', ' ', text)

        return text[:30000]