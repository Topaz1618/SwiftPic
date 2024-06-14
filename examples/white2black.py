from PIL import Image


def convert_white_to_black(image_path):
    # 打开图像
    img = Image.open(image_path)
    img = img.convert("RGBA")  # 确保图像是RGBA格式（带透明通道）

    # 加载图像数据
    data = img.getdata()

    # 创建一个新的图像数据列表
    new_data = []
    for item in data:
        # 改变所有白色（并非完全白色，可能需要调整阈值）的像素为黑色
        if item[0] > 200 and item[1] > 200 and item[2] > 200:  # 这里检测的是接近白色的像素
            new_data.append((0, 0, 0, item[3]))  # 更改为黑色，保持原有的alpha值
        else:
            new_data.append(item)  # 其他颜色保持不变

    # 更新图像数据
    img.putdata(new_data)

    # 保存或显示图像
    img.save('output.png')  # 保存到文件
    img.show()  # 直接显示图像


# 使用图像路径调用函数
convert_white_to_black('toto_footer2.png')
