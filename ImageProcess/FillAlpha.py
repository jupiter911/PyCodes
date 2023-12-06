from PIL import Image
import os
import queue

def flood_fill(image, x, y, fill_color, target_color, transparency_threshold):
    width, height = image.size
    visited = set()

    q = queue.Queue()
    q.put((x, y))

    while not q.empty():
        cx, cy = q.get()

        if (
            0 <= cx < width
            and 0 <= cy < height
            and (cx, cy) not in visited
            and color_difference(image.getpixel((cx, cy)), target_color) <= transparency_threshold
        ):
            image.putpixel((cx, cy), fill_color)
            visited.add((cx, cy))

            q.put((cx + 1, cy))
            q.put((cx - 1, cy))
            q.put((cx, cy + 1))
            q.put((cx, cy - 1))

def color_difference(color1, color2):
    return sum(abs(a - b) for a, b in zip(color1, color2))

def process_images(input_folder, output_folder, fill_color=(255, 255, 255), transparency_threshold=30):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有png图片
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 打开图片
            image = Image.open(input_path)

            # 获取图片的大小
            width, height = image.size

            # 将图片上下左右边界的X或Y的距离填充为指定颜色
            image = image.crop((1, 1, width - 1, height - 1))
            original_image = Image.new("RGBA", (width, height), fill_color)
            original_image.paste(image, (1, 1))

            # 选择一个种子点，可以根据需要自行调整
            seed_point = (0, 0)

            # 使用种子填充算法
            flood_fill(original_image, seed_point[0], seed_point[1], (0, 0, 0, 0), fill_color, transparency_threshold)

            # 保存处理后的图片到输出文件夹
            original_image.save(output_path)

if __name__ == "__main__":
    input_folder = r"D:\ImageCenter\slied2\test"
    output_folder = os.path.join(input_folder, "Out")

    process_images(input_folder, output_folder)
