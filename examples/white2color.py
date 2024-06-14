from PIL import Image


def hex_to_rgb(hex_color):
    # 从HEX颜色代码（例如"#FFFFFF"）转换为RGB格式
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def convert_white_to_fixed_color(image_path, hex_color):
    # 将HEX颜色转换为RGB
    new_color = hex_to_rgb(hex_color)

    # 打开图像
    img = Image.open(image_path)
    img = img.convert("RGBA")  # 确保图像是RGBA格式（带透明通道）

    # 加载图像数据
    data = img.getdata()

    # 创建一个新的图像数据列表
    new_data = []
    for item in data:
        # 如果像素接近白色，则赋予新的固定颜色
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            # 新的颜色，保持原有的alpha值
            new_data.append(new_color + (item[3],))
        else:
            new_data.append(item)  # 其他颜色保持不变

    # 更新图像数据
    img.putdata(new_data)

    # 保存或显示图像
    img.save('output_fixed_color.png')
    img.show()


# 使用图像路径和新的HEX颜色代码调用函数
convert_white_to_fixed_color('toto_footer2.png', '#6747c7')  # 红色