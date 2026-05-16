# =========================================================
# FILE: app/services/ai/ocr_service.py
# =========================================================

import pytesseract

from PIL import Image, ImageFilter, ImageEnhance

from pdf2image import convert_from_path

from docx import Document

from PyPDF2 import PdfReader


class OCRService:

    # =================================================
    # PREPROCESS IMAGE
    # =================================================
    @staticmethod
    def preprocess_image(image):

        # grayscale
        image = image.convert('L')

        # tăng tương phản
        enhancer = ImageEnhance.Contrast(image)

        image = enhancer.enhance(2.5)

        # sharpen
        image = image.filter(
            ImageFilter.SHARPEN
        )

        # threshold
        image = image.point(
            lambda x: 0 if x < 160 else 255,
            '1'
        )

        return image

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

                image = OCRService.preprocess_image(
                    image
                )

                text = pytesseract.image_to_string(
                    image,
                    lang='vie',
                    config='--psm 6'
                )



            # =================================================
            # PDF
            # =================================================

            elif extension == 'pdf':

                try:

                    reader = PdfReader(file_path)

                    pdf_text = ""

                    for page in reader.pages:

                        page_content = page.extract_text()

                        if page_content:

                            pdf_text += (
                                page_content + "\n"
                            )

                    # =========================================
                    # nếu đọc được text thật
                    # =========================================
                    if len(pdf_text.strip()) > 300:

                        text = pdf_text

                    # =========================================
                    # fallback OCR
                    # =========================================
                    else:

                        raise Exception()

                except Exception:

                    pages = convert_from_path(
                        file_path,
                        dpi=300
                    )

                    for page in pages:

                        page = OCRService.preprocess_image(
                            page
                        )

                        page_text = pytesseract.image_to_string(
                            page,
                            lang='vie',
                            config='--oem 3 --psm 6'
                        )

                        text += page_text + "\n"


            # =================================================
            # DOCX
            # =================================================
            elif extension == 'docx':

                doc = Document(file_path)

                for paragraph in doc.paragraphs:

                    if paragraph.text.strip():

                        text += (
                            paragraph.text + "\n"
                        )

            # =================================================
            # TXT
            # =================================================
            elif extension == 'txt':

                with open(
                    file_path,
                    'r',
                    encoding='utf-8'
                ) as file:

                    text = file.read()

            # =================================================
            # CLEAN OCR NOISE
            # =================================================
            text = text.replace('|', 'I')

            text = text.replace('“', '"')

            text = text.replace('”', '"')

            return text.strip()

        except Exception as e:

            print("OCR ERROR:", e)

            return ""