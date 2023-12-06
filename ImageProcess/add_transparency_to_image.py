import cv2
import numpy as np
import os

# 输入文件夹和输出文件夹的默认路径
input_folder = r"D:\ImageCenter\Input"
output_folder = r"D:\ImageCenter\Output"

# 检查输出文件夹是否存在，如果不存在则创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取输入文件夹中的所有图像文件
image_files = [file for file in os.listdir(input_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

# 阈值，控制像素是否被视为足够白
threshold = 200  # 调整阈值，根据需要修改

# 遍历每个图像文件
for image_file in image_files:
    # 构建输入图像的完整路径
    input_image_path = os.path.join(input_folder, image_file)

    # 读取图像，确保图像是带有透明通道（alpha通道）的PNG图像
    image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)

    # 如果图像不包含透明通道，可以添加一个透明通道
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # 将不够白的像素的透明度设置为0
    non_white_pixels = (image[:, :, 0] < threshold) & (image[:, :, 1] < threshold) & (image[:, :, 2] < threshold)
    image[non_white_pixels, 3] = 0  # 设置透明度为0

    # 构建输出图像的完整路径
    output_image_path = os.path.join(output_folder, image_file)

    # 如果输出文件已存在，覆盖保存
    if os.path.exists(output_image_path):
        os.remove(output_image_path)

    # 保存处理后的图像
    cv2.imwrite(output_image_path, image)

    print(f"已处理并保存图像: {image_file}")

print("所有图像处理完成。")
