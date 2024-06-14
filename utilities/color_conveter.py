import base64
from io import BytesIO

from PIL import Image, ImageOps


class ColorConverter:
    def __init__(self, img):
        self.img = img.convert("RGBA")

    def _hex_to_rgb(self, hex_color):
        # 从HEX颜色代码（例如"#FFFFFF"）转换为RGB格式
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def convert_black_to_color(self, hex_color):

        custom_color = self._hex_to_rgb(hex_color)

        data = self.img.getdata()
        new_data = []
        for item in data:
            if item[0] < 50 and item[1] < 50 and item[2] < 50:  # 检测接近黑色的像素
                new_data.append(custom_color + (item[3],))  # 替换为自定义颜色，保持alpha值
            else:
                new_data.append(item)
        self.img.putdata(new_data)
        return self.img

    def convert_white_to_color(self, hex_color):

        custom_color = self._hex_to_rgb(hex_color)

        data = self.img.getdata()
        new_data = []
        for item in data:
            if item[0] > 200 and item[1] > 200 and item[2] > 200:  # 检测接近白色的像素
                new_data.append(custom_color + (item[3],))  # 替换为自定义颜色，保持alpha值
            else:
                new_data.append(item)
        self.img.putdata(new_data)
        return self.img

    def convert_black_to_white(self):
        data = self.img.getdata()
        new_data = []
        for item in data:
            if item[0] < 50 and item[1] < 50 and item[2] < 50:  # 检测接近黑色的像素
                new_data.append((255, 255, 255, item[3]))  # 黑色转白色
            else:
                new_data.append(item)
        self.img.putdata(new_data)
        return self.img

    def convert_white_to_black(self):
        data = self.img.getdata()
        new_data = []
        for item in data:
            if item[0] > 200 and item[1] > 200 and item[2] > 200:  # 检测接近白色的像素
                new_data.append((0, 0, 0, item[3]))  # 白色转黑色
            else:
                new_data.append(item)
        self.img.putdata(new_data)
        return self.img

    def invert_colors(self):
        inverted_img = ImageOps.invert(self.img.convert('RGB'))  # 反转图像颜色（先转换为 RGB 模式）
        inverted_img.putalpha(self.img.getchannel('A'))  # 使用原始图像的 alpha 通道
        return inverted_img.convert('RGBA')  # 转回 RGBA 模式

    def get_base64_image(self):
        img_byte_array = BytesIO()
        self.img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        img_base64 = base64.b64encode(img_byte_array.read()).decode('utf-8')
        return img_base64

    def save_image(self, output_path):
        self.img.save(output_path)

    def show_image(self):
        self.img.show()


if __name__ == "__main__":
    image_path = "../examples/toto_footer2.png"
    img = Image.open(image_path).convert("RGBA")
    color_converter = ColorConverter(img)
    color_converter.convert_white_to_color("#6747c7")
    color_converter.show_image()

