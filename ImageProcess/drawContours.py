import cv2
import numpy as np
import os

# 输入和输出文件夹路径
input_folder = r"D:\ImageCenter\temp2"
output_folder = r"D:\ImageCenter\temp3"

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# 列出输入文件夹中的所有图片文件
image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

for image_file in image_files:
    # 读取图像
    image_path = os.path.join(input_folder, image_file)
    image = cv2.imread(image_path)

    # 阈值化，将白色部分设置为255，其他部分为0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # 找到白色像素的坐标
    white_pixels = np.where(thresh == 255)

    # 计算白色像素的质心
    if len(white_pixels[0]) > 0:
        cx = int(np.mean(white_pixels[1]))  # x坐标取白色像素x坐标的平均值
        cy = int(np.mean(white_pixels[0]))  # y坐标取白色像素y坐标的平均值

        # 获取图像中心
        height, width = image.shape[:2]
        image_center = (width // 2, height // 2)

        # 计算偏移量
        offset_x = image_center[0] - cx  # X轴偏移量
        offset_y = image_center[1] - cy  # Y轴偏移量

        # 创建一个新图像，保持原有大小
        new_image = np.zeros_like(image)

        # 计算粘贴区域的坐标
        paste_x1 = max(0, offset_x)
        paste_x2 = min(width, offset_x + width)
        paste_y1 = max(0, offset_y)
        paste_y2 = min(height, offset_y + height)

        # 计算源图像的坐标
        src_x1 = max(0, -offset_x)
        src_x2 = min(width - offset_x, width)
        src_y1 = max(0, -offset_y)
        src_y2 = min(height - offset_y, height)

        # 将源图像内容粘贴到新图像的正确位置
        new_image[paste_y1:paste_y2, paste_x1:paste_x2] = image[src_y1:src_y2, src_x1:src_x2]

        # 构建输出文件路径
        output_path = os.path.join(output_folder, image_file)

        # 保存结果图像
        cv2.imwrite(output_path, new_image)
    else:
        print(f"警告：图像 {image_file} 中没有白色像素。")

print("所有图像中的白色部分已调整到中心并保存到 centered_images 文件夹中。")
