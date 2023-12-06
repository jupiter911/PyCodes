from PIL import Image
import os

# 输入文件夹路径
input_folder = r"E:\txt2img-images"

# 输出文件夹路径
output_folder = r"E:\Assets\Out"

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    # 检查文件扩展名以确定是否为图像文件
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # 构建输入文件的完整路径
        input_path = os.path.join(input_folder, filename)

        # 打开图像
        image = Image.open(input_path)

        # 将图像转换为灰度
        gray_image = image.convert("L")

        # 构建输出文件的完整路径
        output_path = os.path.join(output_folder, filename)

        # 保存灰度图像
        gray_image.save(output_path)

print("转换完成")
