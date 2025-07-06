import fitz  # PyMuPDF
import os

def pdf_to_png(pdf_path, page_numbers, output_folder):
    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)
    
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历指定的页数
    for page_number in page_numbers:
        # 获取页面
        page = pdf_document.load_page(page_number - 1)  # 页码从0开始
        # 将页面转换为图像
        pix = page.get_pixmap()
        # 保存图像
        output_path = os.path.join(output_folder, f"page_{page_number}.png")
        pix.save(output_path)
        print(f"Page {page_number} saved as {output_path}")

    # 关闭PDF文件
    pdf_document.close()

# 示例用法
pdf_path = input("请输入PDF文件路径: ").strip().strip('"').strip("'")
page_numbers = input("请输入要转换的页码（用逗号分隔）: ")
page_numbers = [int(num.strip()) for num in page_numbers.split(',')]
output_folder = "output_images"

pdf_to_png(pdf_path, page_numbers, output_folder)