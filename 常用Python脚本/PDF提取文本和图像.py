import fitz  # PyMuPDF
import os

# 提取PDF中的文本

def extract_text_from_pdf(pdf_path):
    try:
        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)
        text = ""
        
        # 遍历每一页
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        print(f"提取文本失败: {str(e)}")
        return None

# 提取PDF中的图像

def extract_images_from_pdf(pdf_path, output_folder):
    try:
        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)
        
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 遍历每一页
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            images = page.get_images(full=True)
            
            # 提取每个图像
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image['image']
                image_ext = base_image['ext']
                image_path = os.path.join(output_folder, f"page_{page_num+1}_img_{img_index+1}.{image_ext}")
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                print(f"Image saved as {image_path}")
        pdf_document.close()
    except Exception as e:
        print(f"提取图像失败: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    pdf_file = input('请输入PDF文件路径：').strip().strip('"\'')
    output_folder = input('请输入图像输出文件夹路径：').strip().strip('"\'')
    
    # 检查文件是否存在
    if not os.path.exists(pdf_file):
        print('错误：文件不存在！')
    else:
        # 提取文本
        text = extract_text_from_pdf(pdf_file)
        if text:
            print("提取的文本内容：")
            print(text)
        
        # 提取图像
        extract_images_from_pdf(pdf_file, output_folder)