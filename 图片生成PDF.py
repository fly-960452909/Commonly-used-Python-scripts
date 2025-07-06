import os
from PIL import Image
from reportlab.pdfgen import canvas

# 获取文件夹中的所有图片文件
image_folder = input("请输入图片文件夹路径: ").strip().strip('"').strip("'")
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]

# 提供选项让用户选择图片顺序
order_choice = input("请选择图片顺序: 1. 文件名排序 2. 自定义顺序 (输入1或2): ").strip()

if order_choice == '2':
    # 列出文件编号和名称
    for index, image_file in enumerate(image_files):
        print(f"{index + 1}: {image_file}")
    
    # 提示用户根据编号输入顺序
    custom_order = input("请输入图片文件编号顺序（用逗号分隔）: ").strip()
    image_files = [image_files[int(i.strip()) - 1] for i in custom_order.split(',') if i.strip().isdigit() and 0 < int(i.strip()) <= len(image_files)]
    if len(image_files) != len(custom_order.split(',')):
        print("警告: 输入的编号中有无效编号。")
    else:
        print("所有输入的编号都有效。")
else:
    image_files.sort()

# 创建PDF文件
output_pdf_path = os.path.join(image_folder, "output.pdf")
c = canvas.Canvas(output_pdf_path)

# 遍历图片文件并添加到PDF
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    try:
        img = Image.open(image_path)
        c.setPageSize(img.size)
        c.drawImage(image_path, 0, 0)
        c.showPage()
    except Exception as e:
        print(f"无法处理图片 {image_file}: {str(e)}")

# 保存PDF文件
c.save()
print(f"PDF文件已保存到: {output_pdf_path}")