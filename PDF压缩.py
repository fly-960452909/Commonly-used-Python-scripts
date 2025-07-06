import fitz  # PyMuPDF
import os

# 压缩PDF文件

def compress_pdf(input_pdf_path, output_pdf_path, quality=75):
    try:
        # 打开PDF文件
        pdf_document = fitz.open(input_pdf_path)
        
        # 创建输出PDF文件
        pdf_document.save(output_pdf_path, garbage=4, deflate=True, clean=True)
        pdf_document.close()
        print(f"PDF文件已压缩并保存到: {output_pdf_path}")
    except Exception as e:
        print(f"压缩失败: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    input_pdf = input('请输入要压缩的PDF文件路径：').strip().strip('"\'')
    output_pdf = input('请输入输出PDF文件路径：').strip().strip('"\'')
    
    # 检查文件是否存在
    if not os.path.exists(input_pdf):
        print('错误：输入文件不存在！')
    else:
        # 执行压缩
        compress_pdf(input_pdf, output_pdf)