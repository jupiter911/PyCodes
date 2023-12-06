import cv2
import numpy as np
import os

# 控制参数
calculate_alpha = True  # 是否计算 alpha 通道
alpha_threshold = 100  # 当计算 alpha 通道时，alpha 值的阈值
is_white = False  # 是否判断白色
fillWithWhite = True

def process_image(image_path, output_folder, calculate_alpha, alpha_threshold, is_white):
    # 读取图像
    image = cv2.imread(image_path)
    originImage = cv2.imread(image_path,cv2.IMREAD_UNCHANGED)

    if(calculate_alpha):
        # 转换为带有Alpha通道的图像
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        # 找到 alpha 通道为 0 的像素
        zero_alpha_pixels = (image[:, :, 3] < alpha_threshold)

        # 将 alpha 为 0 的像素转换为反色
        image[zero_alpha_pixels, :4] = [0,0,0,255] if is_white else [255, 255, 255,255]
        #originImage[zero_alpha_pixels, :4] = [0,0,0,255] if is_white else [255, 255, 255,255]

    # 阈值化处理
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY if is_white else cv2.THRESH_BINARY_INV)


    # 找到白色（或黑色）像素的坐标
    white_pixels = np.where(thresh == 255)

    # 检查图像是否包含有效的白色（或黑色）像素
    if len(white_pixels[0]) > 0:
        # 计算白色（或黑色）像素的质心
        cx = int(np.mean(white_pixels[1]))  # x坐标取白色（或黑色）像素x坐标的平均值
        cy = int(np.mean(white_pixels[0]))  # y坐标取白色（或黑色）像素y坐标的平均值

        # 获取图像中心
        height, width = image.shape[:2]
        image_center = (width // 2, height // 2)

        # 计算偏移量（按照你的代码）
        offset_x = image_center[0] - cx# if is_white else cx - image_center[0]  # X轴偏移量
        offset_y = image_center[1] - cy# if is_white else cy - image_center[1]  # Y轴偏移量

        # 创建一个新图像，保持原有大小
        new_image = np.zeros((height, width, 4), dtype=np.uint8)

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

        if(calculate_alpha and not fillWithWhite):
            new_image[paste_y1:paste_y2, paste_x1:paste_x2, :4] = originImage[src_y1:src_y2, src_x1:src_x2, :4]

        else:
            # 将原图像内容粘贴到新图像的中央位置
            new_image[:, :, 3] = 255
            new_image[paste_y1:paste_y2, paste_x1:paste_x2, :3] = image[src_y1:src_y2, src_x1:src_x2, :3]

        # 设置未被覆盖的区域透明
        custom_color = (255, 255, 255, 0 if (calculate_alpha and not fillWithWhite) else 255)
        new_image[:paste_y1, :] = custom_color  # 顶部未覆盖区域设为透明
        new_image[paste_y2:, :] = custom_color  # 底部未覆盖区域设为透明
        new_image[:, :paste_x1] = custom_color  # 左侧未覆盖区域设为透明
        new_image[:, paste_x2:] = custom_color  # 右侧未覆盖区域设为透明

        #new_image[image_center] = [255,0,0,255]
        #new_image[cx,cy] = [0,255,0,255]
        # 构建输出文件路径
        output_path = os.path.join(output_folder, os.path.basename(image_path))

        # 保存结果图像
        cv2.imwrite(output_path, new_image)

# 示例用法
input_folder_path = r"D:\ImageCenter\GoodIcons1"
output_folder_path = os.path.join(input_folder_path, "Out")

# 创建输出文件夹
if not os.path.exists(output_folder_path):
    os.mkdir(output_folder_path)


# 遍历文件夹中的所有PNG文件
for file_name in os.listdir(input_folder_path):
    if file_name.lower().endswith(".png"):
        file_path = os.path.join(input_folder_path, file_name)
        process_image(file_path, output_folder_path, calculate_alpha, alpha_threshold, is_white)

print("处理完成！")