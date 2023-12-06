from PIL import Image

# 打开PNG文件
png_image = Image.open(r'F:\VuePressProjects\Abyss_Descenders\src\.vuepress\public\assets\image\Head1.png')

# 将PNG文件保存为ICO文件
png_image.save(r'F:\VuePressProjects\Abyss_Descenders\src\.vuepress\public\favicon.ico')
