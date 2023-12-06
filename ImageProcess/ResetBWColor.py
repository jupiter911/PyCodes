from PIL import Image
import os

# 输入文件夹路径
input_folder = r"E:\Assets\In"

# 输出文件夹路径
output_folder = r"E:\Assets\Out"

# 档位数量
N = 8

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    # 检查文件扩展名以确定是否为图像文件
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # 构建输入文件的完整路径
        input_path = os.path.join(input_folder, filename)

        # 打开灰度图像
        gray_image = Image.open(input_path)

        # 获取图像的像素数据
        pixels = list(gray_image.getdata())

        # 将像素颜色重新调整到N个档位
        adjusted_pixels = [int(((pixel + 1) // N)+1) * N for pixel in pixels]

        # 创建新图像
        adjusted_image = Image.new("L", gray_image.size)
        adjusted_image.putdata(adjusted_pixels)

        # 构建输出文件的完整路径
        output_path = os.path.join(output_folder, filename)

        # 保存调整后的图像
        adjusted_image.save(output_path)

print("调整完成")
