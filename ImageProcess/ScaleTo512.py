from PIL import Image
import os

def resize_images(input_folder, output_folder, target_size=(512, 512)):
    # 遍历文件夹中的所有PNG文件
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".png"):
            file_path = os.path.join(input_folder, file_name)

            # 打开图像
            image = Image.open(file_path)

            # 缩放图像
            resized_image = image.resize(target_size, Image.BILINEAR)

            # 创建输出文件夹，如果不存在的话
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # 生成输出文件路径
            output_path = os.path.join(output_folder, file_name)

            # 保存缩放后的图像
            resized_image.save(output_path)

# 示例用法
input_folder_path = r"E:\UnityProject\游戏素材\AI抠图\icons1"  # 请替换为你的输入文件夹路径
output_folder_path = r"E:\UnityProject\游戏素材\AI抠图\icons1_512"  # 请替换为你的输出文件夹路径

resize_images(input_folder_path, output_folder_path)
