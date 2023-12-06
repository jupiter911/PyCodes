from PIL import Image
import os

def has_nonzero_alpha(pixel):
    # 判断一个像素是否包含透明度不为0
    return pixel[3] != 0

def crop_non_black_images(image_path, output_directory,slice_sizeX,slice_sizeY):
    # 打开图像
    image = Image.open(image_path)

    # 获取图像大小
    width, height = image.size

    # 初始化切图计数器
    slice_counter = 0

    # 遍历图像并切图
    for y in range(0, height, slice_sizeY):
        for x in range(0, width, slice_sizeX):
            # 获取当前切割块
            slice_box = (x, y, x + slice_sizeX, y + slice_sizeY)
            slice_image = image.crop(slice_box)

            # 检查切割块是否包含透明度不为0的像素
            nonzero_alpha_found = any(has_nonzero_alpha(slice_image.getpixel((i, j))) for i in range(slice_sizeX) for j in range(slice_sizeY))

            # 如果包含透明度不为0的像素，则保存切割块
            if nonzero_alpha_found:
                output_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(image_path))[0]}_slice_{slice_counter}.png")
                slice_image.save(output_path)
                slice_counter += 1

def process_folder(input_folder, output_folder,slice_sizeX,slice_sizeY):
    # 遍历文件夹中的所有PNG文件
    for file_name in os.listdir(input_folder):

        if file_name.lower().endswith(".png"):
            file_path = os.path.join(input_folder, file_name)

            # 创建输出文件夹，如果不存在的话
            output_directory = os.path.join(output_folder, f'{os.path.splitext(file_name)[0]}')
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            crop_non_black_images(file_path, output_directory,slice_sizeX,slice_sizeY)

def process_File(input_File,output_folder,slice_sizeX,slice_sizeY):
    if input_File.lower().endswith(".png"):

        # 创建输出文件夹，如果不存在的话
        output_directory = os.path.join(output_folder, f'{os.path.splitext(input_File)[0]}')
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        crop_non_black_images(input_File, output_directory,slice_sizeX,slice_sizeY)
    
# 示例用法
# input_folder_path = r"E:\UnityProject\DEMO_NEW_URP\Assets\SpriteCuter\icons1"  # 请替换为你的输入文件夹路径
# output_folder_path = r"F:\MyPythonCodes\slice"  # 请替换为你的输出文件夹路径

# process_folder(input_folder_path, output_folder_path,256)
