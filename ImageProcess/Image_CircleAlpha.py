from PIL import Image, ImageDraw
import os

# 默认输入文件夹路径
input_folder = r"E:\Assets\In"

# 默认输出文件夹路径
output_folder = r"E:\Assets\Out"

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历默认输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    # 检查文件扩展名以确定是否为图像文件
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # 构建输入文件的完整路径
        input_path = os.path.join(input_folder, filename)

        # 打开灰度图像
        gray_image = Image.open(input_path).convert("L")

        # 获取图像的宽度和高度
        width, height = gray_image.size

        # 创建一个新的彩色图像，带有透明通道
        new_image = Image.new("RGBA", (width, height))

        # 创建一个绘图对象
        draw = ImageDraw.Draw(new_image)

        # 计算圆的半径
        radius = width / 2

        # 计算圆心坐标
        center = (width / 2, height / 2)

        # 遍历图像的每个像素
        for x in range(width):
            for y in range(height):
                # 计算像素点到圆心的距离
                distance = ((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5

                # 如果距离大于半径，将像素的alpha通道设为0
                if distance > radius:
                    new_image.putpixel((x, y), (0, 0, 0, 0))
                else:
                    # 否则，使用灰度值创建彩色像素
                    gray_value = gray_image.getpixel((x, y))
                    new_pixel = (gray_value, gray_value, gray_value, 255)  # R, G, B, A
                    new_image.putpixel((x, y), new_pixel)

        # 构建输出文件的完整路径
        output_path = os.path.join(output_folder, filename)

        # 保存处理后的图像
        new_image.save(output_path, "PNG")

print("处理完成")
