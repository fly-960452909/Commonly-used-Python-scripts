import PyPDF2
import os

# 旋转PDF页面

def rotate_pdf_pages(input_pdf_path, output_pdf_path, rotation_angle):
    try:
        # 打开PDF文件
        with open(input_pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            # 旋转每一页
            for page in reader.pages:
                page.rotate_clockwise(rotation_angle)
                writer.add_page(page)
            
            # 写入旋转后的PDF
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
            print(f"PDF文件已旋转并保存到: {output_pdf_path}")
    except Exception as e:
        print(f"旋转失败: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    input_pdf = input('请输入PDF文件路径：').strip().strip('"\'')
    output_pdf = input('请输入输出PDF文件路径：').strip().strip('"\'')
    rotation_angle = int(input('请输入旋转角度（90, 180, 270）：').strip())
    
    # 检查文件是否存在
    if not os.path.exists(input_pdf):
        print('错误：输入文件不存在！')
    else:
        # 执行旋转
        rotate_pdf_pages(input_pdf, output_pdf, rotation_angle)