import cv2
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
import os

# 默认的保存文件夹路径
default_output_folder = "F:/MyPythonCodes/Temp/Output"

# 检查文件夹是否存在，如果不存在则创建
if not os.path.exists(default_output_folder):
    os.makedirs(default_output_folder)

# 图片处理函数
def process_image(input_path, output_folder, threshold_black, threshold_white):
    try:
        image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            status_label.config(text=f"无法读取图像：{input_path}")
            return

        if image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        black_pixels = (image[:, :, 0] <= threshold_black) & (image[:, :, 1] <= threshold_black) & (image[:, :, 2] <= threshold_black)
        white_pixels = (image[:, :, 0] >= threshold_white) & (image[:, :, 1] >= threshold_white) & (image[:, :, 2] >= threshold_white)
        non_white_black_pixels = black_pixels | white_pixels
        image[non_white_black_pixels, 3] = 0

        # 获取输入文件的文件名
        file_name = os.path.basename(input_path)

        # 构建输出文件的完整路径
        output_path = os.path.join(output_folder, file_name)
        cv2.imwrite(output_path, image)
        status_label.config(text=f"已处理并保存图像：{output_path}")
    except Exception as e:
        status_label.config(text=f"处理图像时出现错误：{str(e)}")

# 拖拽事件处理函数
def on_drop(event):
    input_path = event.data
    output_folder = output_path_entry.get()
    threshold_black = int(threshold_black_entry.get())
    threshold_white = int(threshold_white_entry.get())
    
    process_image(input_path, output_folder, threshold_black, threshold_white)

# 打开文件夹对话框以选择保存文件夹路径
def select_output_folder():
    output_folder = filedialog.askdirectory(initialdir=default_output_folder)
    output_path_entry.delete(0, tk.END)
    output_path_entry.insert(0, output_folder)

# 创建主窗口
root = TkinterDnD.Tk()
root.title("图片处理")

# 创建拖拽区域
drop_label = tk.Label(root, text="拖拽图片到此区域")
drop_label.pack(pady=20)
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind('<<Drop>>', on_drop)

# 创建保存文件夹选择框
output_path_label = tk.Label(root, text="保存文件夹：")
output_path_label.pack()
output_path_entry = tk.Entry(root, width=50)
output_path_entry.insert(0, default_output_folder)
output_path_entry.pack()
output_path_button = tk.Button(root, text="选择文件夹", command=select_output_folder)
output_path_button.pack()

# 创建黑色阈值输入框
threshold_black_label = tk.Label(root, text="黑色阈值：")
threshold_black_label.pack()
threshold_black_entry = tk.Entry(root)
threshold_black_entry.insert(0, "0")
threshold_black_entry.pack()

# 创建白色阈值输入框
threshold_white_label = tk.Label(root, text="白色阈值：")
threshold_white_label.pack()
threshold_white_entry = tk.Entry(root)
threshold_white_entry.insert(0, "255")
threshold_white_entry.pack()

# 创建状态标签
status_label = tk.Label(root, text="")
status_label.pack(pady=20)

root.mainloop()
