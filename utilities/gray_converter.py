# image_processor.py
import io
import base64
from PIL import Image


class GrayImageProcessor:
    def img_converter(self, img):
        img = img.convert('L')
        return img

    def process_image(self, image_path, output_path):
        img = Image.open(image_path)

        # Convert image to grayscale
        img = self.img_converter(img)

        # Save processed image
        img.save(output_path, format="JPEG")

        return output_path

    def process_bytes(self, image_bytes):
        img = self.img_converter(image_bytes)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return buffered.getvalue()


# 如果单独执行这个文件，则进行测试
if __name__ == "__main__":
    input_image_path = "imgs/input.jpg"
    output_image_path = "results/gray_output.png"
    processor = GrayImageProcessor()
    processor.process_image(input_image_path, output_image_path)