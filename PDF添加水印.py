import PyPDF2
import os

# 添加水印到PDF文件

def add_watermark(input_pdf_path, output_pdf_path, watermark_pdf_path):
    try:
        # 打开PDF文件
        with open(input_pdf_path, 'rb') as input_file, open(watermark_pdf_path, 'rb') as watermark_file:
            reader = PyPDF2.PdfReader(input_file)
            watermark_reader = PyPDF2.PdfReader(watermark_file)
            writer = PyPDF2.PdfWriter()
            
            # 获取水印页面
            watermark_page = watermark_reader.pages[0]
            
            # 为每一页添加水印
            for page in reader.pages:
                page.merge_page(watermark_page)
                writer.add_page(page)
            
            # 写入带水印的PDF
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
            print(f"水印已添加并保存到: {output_pdf_path}")
    except Exception as e:
        print(f"添加水印失败: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    input_pdf = input('请输入PDF文件路径：').strip().strip('"\'')
    output_pdf = input('请输入输出PDF文件路径：').strip().strip('"\'')
    watermark_pdf = input('请输入水印PDF文件路径：').strip().strip('"\'')
    
    # 检查文件是否存在
    if not os.path.exists(input_pdf) or not os.path.exists(watermark_pdf):
        print('错误：输入文件或水印文件不存在！')
    else:
        # 执行添加水印
        add_watermark(input_pdf, output_pdf, watermark_pdf)