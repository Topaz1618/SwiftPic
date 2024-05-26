import re
import pdfplumber
import pytesseract
import easyocr
import cv2
import numpy as np


def demo(filename):
    with pdfplumber.open(filename) as pdf:
        ocr_text = ""
        # reader = easyocr.Reader(['ch_sim', 'en'])  # this needs to run only once to load the model into memory
        for page_num, page in enumerate(pdf.pages):
            default_text = page.extract_text()
            print(f"Page: {page_num} default_text: {default_text}\n ")

            # img = page.to_image()
            # img_cv = cv2.cvtColor(np.array(img.original), cv2.COLOR_RGB2BGR)

            # easyocr 中文可以，英文一般
            # result = reader.readtext(img_cv)
            # ocr_text += ' '.join([res[1] for res in result])
            # print(ocr_text)

    print(ocr_text)


if __name__ == "__main__":
    demo('a.pdf')
