import easyocr
from PIL import Image

# 加载图像
image_path = 'a5.png'
image = Image.open(image_path)

# 初始化OCR阅读器，指定语言
reader = easyocr.Reader(['ch_sim', 'en'])  # 如果需要支持中文，可以使用 ['ch_sim', 'en']

# 执行OCR识别
results = reader.readtext(image_path)

# 打印识别结果
ocr_text = ""
for (bbox, text, prob) in results:
    ocr_text += text

print(f"Detected text: {ocr_text} ")