from PIL import Image, ImageDraw
import os

# 默认输入文件夹路径
input_folder = r"E:\Assets\In"

# 默认输出文件夹路径
output_folder = r"E:\Assets\Out"

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取所有PNG文件的文件名
png_files = [f for f in os.listdir(input_folder) if f.endswith(".png")]

threshold1=80
threshold2=220

# 遍历所有PNG文件
for filename in png_files:
    # 构建输入文件的完整路径
    input_image_path = os.path.join(input_folder, filename)

    # 构建输出文件的完整路径
    output_image_path = os.path.join(output_folder, filename)

    # 打开彩色图像
    image = Image.open(input_image_path)

    # 获取图像的宽度和高度
    width, height = image.size

    # 计算圆的半径
    radius = width / 2

    # 创建一个新的图像，带有透明通道
    new_image = Image.new("RGBA", (width, height))

    # 创建一个绘图对象
    draw = ImageDraw.Draw(new_image)

    # 计算圆心坐标
    center = (width / 2, height / 2)

    # 遍历图像的每个像素
    for x in range(width):
        for y in range(height):
            # 计算像素点到圆心的距离
            distance = ((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5

            # 获取原始像素的颜色值
            pixel = image.getpixel((x, y))

            # 检查是否包含透明通道
            if len(pixel) == 3:
                # 如果没有透明通道，添加默认的透明通道值
                pixel += (255,)

            # 解包颜色值
            r, g, b, a = pixel

            # 计算灰度值
            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)

            # 根据灰度值应用阈值
            if distance <= radius:
                if gray_value < threshold1:
                    new_pixel = (0, 0, 0, a)  # 黑色
                elif gray_value > threshold2:
                    new_pixel = (255, 255, 255, a)  # 白色
                else:
                    new_pixel = (gray_value, gray_value, gray_value, a)  # 保持原始颜色
            else:
                new_pixel = (r, g, b, 0)  # 在圆外的部分，透明

            new_image.putpixel((x, y), new_pixel)

    # 保存处理后的图像
    new_image.save(output_image_path, "PNG")

print("处理完成")
