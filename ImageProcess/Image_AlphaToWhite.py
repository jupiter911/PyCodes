from PIL import Image
import os

def process_folder(input_folder, output_folder):
    # 遍历文件夹中的所有PNG文件
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".png"):
            file_path = os.path.join(input_folder, file_name)

            # 打开图像
            image = Image.open(file_path)

            # 获取图像大小
            width, height = image.size

            # 创建新图像，将透明像素转换为白色
            new_image = Image.new("RGBA", (width, height), (255, 255, 255, 255))
            new_image.paste(image, (0, 0), image)

            # 保存新图像
            output_path = os.path.join(output_folder, file_name)
            new_image.save(output_path)

if __name__ == "__main__":
    input_folder_path = r"E:\UnityProject\游戏素材\AI抠图\icons1\grid-0132"  # 请替换为你的输入文件夹路径
    output_folder_path = f"{input_folder_path}/Out"  # 请替换为你的输出文件夹路径

    # 创建输出文件夹，如果不存在的话
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 处理文件夹中的PNG文件
    process_folder(input_folder_path, output_folder_path)
