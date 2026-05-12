# =========================================================
# FILE: app/services/ai/ocr_service.py
# =========================================================

import os

import pytesseract

from PIL import Image

from pdf2image import convert_from_path

from docx import Document


class OCRService:

    @staticmethod
    def extract_text(file_path):

        if not file_path:
            return ""

        extension = file_path.split('.')[-1].lower()

        text = ""

        try:

            # =================================================
            # IMAGE OCR
            # =================================================
            if extension in ['png', 'jpg', 'jpeg']:

                image = Image.open(file_path)

                text = pytesseract.image_to_string(
                    image,
                    lang='vie'
                )

            # =================================================
            # PDF OCR
            # =================================================
            elif extension == 'pdf':

                pages = convert_from_path(file_path)

                for page in pages:

                    page_text = pytesseract.image_to_string(
                        page,
                        lang='vie'
                    )

                    text += page_text + "\n"

            # =================================================
            # DOCX READER
            # =================================================
            elif extension == 'docx':

                doc = Document(file_path)

                for paragraph in doc.paragraphs:

                    text += paragraph.text + "\n"

            # =================================================
            # TXT FILE
            # =================================================
            elif extension == 'txt':

                with open(
                    file_path,
                    'r',
                    encoding='utf-8'
                ) as file:

                    text = file.read()

            return text.strip()

        except Exception as e:

            print("OCR ERROR:", e)

            return ""