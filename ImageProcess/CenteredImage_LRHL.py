from PIL import Image
import os

def luminance_threshold(image,use_alpha, use_white):
    # 对图像进行亮度阈值化处理，大于127的点当作白色处理，否则当作黑色处理
    if use_alpha :
        #outColor = 0 if use_white else 255
        return image.split()[-1].point(lambda p: 255 if p > 1 else 0)
    else:
        return image.convert("L").point(lambda p: 255 if p > 127 else 0)
    


def process_image(input_folder, output_folder, use_alpha, use_white, skip_border=0, mark_first_pixel=False):
    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有png文件
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

    for file in input_files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        # 打开图像
        with Image.open(input_path) as img:
            # 对图像进行亮度阈值化处理
            threshold_img = luminance_threshold(img,use_alpha, use_white)

            # 获取图像数据
            threshold_data = threshold_img.getdata()

            # 选择基准色
            base_color_values = 255 if use_alpha else ((255, 255, 255) if use_white else (0, 0, 0))

            # 计算横向平均坐标
            left_base_coord = find_first_pixel(threshold_data, img.width, img.height, base_color_values, skip_border)
            right_base_coord = find_last_pixel(threshold_data, img.width, img.height, base_color_values, skip_border)
            
            if left_base_coord is not None and right_base_coord is not None:
                avg_x = (left_base_coord[0] + right_base_coord[0]) // 2

                # 计算纵向平均坐标
                top_base_coord = find_first_pixel_vertical(threshold_data, img.width, img.height, base_color_values, skip_border)
                bottom_base_coord = find_last_pixel_vertical(threshold_data, img.width, img.height, base_color_values, skip_border)

                if top_base_coord is not None and bottom_base_coord is not None:
                    avg_y = (top_base_coord[1] + bottom_base_coord[1]) // 2

                    # 计算中心点坐标
                    center_x = img.width // 2
                    center_y = img.height // 2

                    # 计算偏移量
                    offset_x = center_x - avg_x
                    offset_y = center_y - avg_y

                    # 创建新的图像对象并用指定颜色填充
                    new_img = Image.new('RGBA', img.size, (0, 0, 0,0) if use_alpha else (255,255,255)if use_white else (0,0,0))  # 这里填充为黑色，可根据需求修改

                    # 将原图复制到新图像对象中
                    new_img.paste(img, (offset_x, offset_y))

                    # 在中心点位置填充红色
                    if mark_first_pixel:
                        new_img.putpixel((left_base_coord[0], left_base_coord[1]), (255, 0, 0))
                        new_img.putpixel((right_base_coord[0], right_base_coord[1]), (255, 0, 0))
                        new_img.putpixel((top_base_coord[0], top_base_coord[1]), (255, 0, 0))
                        new_img.putpixel((bottom_base_coord[0], bottom_base_coord[1]), (255, 0, 0))

                    # 保存新图像
                    new_img.save(output_path)

def find_first_pixel(data, width, height, base_color_values, skip_border=0):
    for x in range(skip_border, width - skip_border):
        for y in range(skip_border, height - skip_border):
            pixel_value = data[y * width + x]

            if pixel_value != 0:  # Check if the pixel is not fully white
                #print(f"pixel_value =={pixel_value},,,base_color_values=={base_color_values}")
                if pixel_value == base_color_values:
                    return x, y

    return None

def find_last_pixel(data, width, height, base_color_values, skip_border=0):
    for x in range(width - 1 - skip_border, skip_border, -1):
        for y in range(height - 1 - skip_border, skip_border, -1):
            pixel_value = data[y * width + x]

            if pixel_value != 0:  # Check if the pixel is not fully white
                if pixel_value == base_color_values:
                    return x, y

    return None

def find_first_pixel_vertical(data, width, height, base_color_values, skip_border=0):
    for y in range(skip_border, height - skip_border):
        for x in range(skip_border, width - skip_border):
            pixel_value = data[y * width + x]

            if pixel_value != 0:  # Check if the pixel is not fully white
                if pixel_value == base_color_values:
                    return x, y

    return None

def find_last_pixel_vertical(data, width, height, base_color_values, skip_border=0):
    for y in range(height - 1 - skip_border, skip_border, -1):
        for x in range(skip_border, width - skip_border):
            pixel_value = data[y * width + x]

            if pixel_value != 0:  # Check if the pixel is not fully white
                if pixel_value == base_color_values:
                    return x, y

    return None

if __name__ == "__main__":
    input_folder = r"D:\ImageCenter\slied2\test\out"  # 输入文件夹路径
    output_folder = os.path.join(input_folder, "out")  # 输出文件夹路径
    use_alpha = True  # False表示以亮度阈值化后的图像进行处理，不考虑alpha通道
    use_white = False  # 不使用白色为基准色，使用亮度阈值化后的图像的黑色为基准色
    skip_border = 5  # 跳过边界的像素数量
    mark_first_pixel = False  # 标记第一个像素点为红色

    process_image(input_folder, output_folder, use_alpha, use_white, skip_border, mark_first_pixel)
