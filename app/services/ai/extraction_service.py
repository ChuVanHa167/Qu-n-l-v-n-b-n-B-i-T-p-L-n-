# =========================================================
# FILE: app/services/ai/extraction_service.py
# =========================================================

import re


class ExtractionService:

    # =====================================================
    # TITLE
    # =====================================================
    @staticmethod
    def extract_title(text):

        if not text:
            return "Không xác định"

        lines = text.split('\n')

        for line in lines:

            line = line.strip()

            if len(line) > 10:

                return line[:255]

        return "Không xác định"

    # =====================================================
    # DOCUMENT NUMBER
    # =====================================================
    @staticmethod
    def extract_document_number(text):

        patterns = [

            r'Số[:\s]+([^\n]+)',

            r'SO[:\s]+([^\n]+)'
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group(1).strip()

        return ""

    # =====================================================
    # ISSUE DATE
    # =====================================================
    @staticmethod
    def extract_issue_date(text):

        pattern = r'(\d{1,2}/\d{1,2}/\d{4})'

        match = re.search(pattern, text)

        if match:

            return match.group(1)

        return ""

    # =====================================================
    # SIGNER
    # =====================================================
    @staticmethod
    def extract_signer(text):

        lines = text.split('\n')

        for line in reversed(lines):

            line = line.strip()

            if (
                len(line) > 5
                and
                len(line) < 50
            ):

                if line.isupper():

                    return line.title()

        return ""

    # =====================================================
    # ISSUER
    # =====================================================
    @staticmethod
    def extract_issuer(text):

        lines = text.split('\n')[:10]

        for line in lines:

            line = line.strip()

            lower = line.lower()

            if (
                'trường' in lower
                or
                'đại học' in lower
                or
                'ubnd' in lower
                or
                'bộ' in lower
            ):

                return line

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

            'biên bản': 'minutes',

            'tờ trình': 'proposal',

            'công văn': 'official_dispatch'
        }

        for keyword, value in mapping.items():

            if keyword in text:

                return value

        return 'other'

    # =====================================================
    # PRIORITY
    # =====================================================
    @staticmethod
    def extract_priority(text):

        text = text.lower()

        if 'hỏa tốc' in text:

            return 'urgent'

        if 'khẩn' in text:

            return 'high'

        return 'normal'

    # =====================================================
    # KEYWORDS
    # =====================================================
    @staticmethod
    def extract_keywords(text):

        text = text.lower()

        found = []

        keywords = [

            'tuyển sinh',
            'học phí',
            'đào tạo',
            'sinh viên',
            'nhân sự',
            'khen thưởng',
            'kỷ luật',
            'tài chính'
        ]

        for keyword in keywords:

            if keyword in text:

                found.append(keyword)

        return ', '.join(found)

    # =====================================================
    # CLEAN CONTENT
    # =====================================================
    @staticmethod
    def clean_content(text):

        if not text:
            return ""

        text = re.sub(r'\n+', '\n', text)

        return text[:10000]