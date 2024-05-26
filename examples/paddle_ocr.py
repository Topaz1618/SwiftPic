from paddleocr import PaddleOCR, draw_ocr
import cv2
from PIL import Image

# 初始化 OCR 模型
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  #  lang='en' 用于英文 lang='ch' 用于中文

# 读取图片
image_path = 'test.png'
image = cv2.imread(image_path)

# 进行 OCR 识别
result = ocr.ocr(image_path, cls=True)

# 打印结果
for line in result:
    print(line)
