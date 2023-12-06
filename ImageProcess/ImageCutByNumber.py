import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import ImageSlicer

class ImageCropper:
    file_path=""

    def __init__(self, master):
        self.master = master
        self.master.title("Image Cropper")
        self.master.geometry("1200x900")

        # 顶部的Frame，包含输入框和按钮
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.x_entry = tk.Entry(self.top_frame, width=5)
        self.x_entry.pack(side=tk.LEFT, padx=5)
        self.y_entry = tk.Entry(self.top_frame, width=5)
        self.y_entry.pack(side=tk.LEFT, padx=5)

        self.crop_button = tk.Button(self.top_frame, text="Crop", command=self.crop_image)
        self.crop_button.pack(pady=5)

        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10, expand=True)

        self.image = None

        # 绑定拖拽事件
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.load_image_from_drop)

    def load_image_from_drop(self, event):
        global file_path
        file_path = event.data
        if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            self.image = Image.open(file_path)
            self.original_size = self.image.size
            self.display_image()

    def display_image(self):
        if self.image:
            # 调整图像大小以适应窗口
            self.image.thumbnail((1200, 900))
            tk_image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image

    def crop_image(self):
        if self.image:
            try:
                x_count = int(self.x_entry.get())
                y_count = int(self.y_entry.get())
                width_interval = self.original_size[0] // x_count
                height_interval = self.original_size[1]  // y_count
                ImageSlicer.process_File(file_path,r"F:\MyPythonCodes\slice",width_interval,height_interval)
                
                tk.messagebox.showinfo("Image Slicer", "Image slicing completed!")

            except ValueError:
                print("Please enter valid X and Y values.")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageCropper(root)
    root.mainloop()
