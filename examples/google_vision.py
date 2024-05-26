import pdfplumber


def ocr_func(filename):
    with pdfplumber.open(filename) as pdf:
        for page_num, page in enumerate(pdf.pages):
            default_text = page.extract_text()
            print(default_text)


ocr_func('Depth-aware Neural Style Transfer.pdf')