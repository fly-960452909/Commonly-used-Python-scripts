from pdf2docx import Converter
import os

def convert_pdf_to_word(pdf_path, word_path=None):
    """
    将PDF文件转换为Word文档
    :param pdf_path: PDF文件路径
    :param word_path: 输出的Word文件路径（可选）
    :return: None
    """
    try:
        # 如果未指定输出路径，则使用原文件名，仅更改扩展名
        if word_path is None:
            word_path = os.path.splitext(pdf_path)[0] + '.docx'
        
        # 创建转换器对象
        cv = Converter(pdf_path)
        # 执行转换
        cv.convert(word_path)
        # 关闭转换器
        cv.close()
        print(f'转换成功！\nPDF文件：{pdf_path}\nWord文件：{word_path}')
        
    except Exception as e:
        print(f'转换失败：{str(e)}')

if __name__ == '__main__':
    # 获取用户输入
    pdf_file = input('请输入PDF文件路径：')
    
    # 去除路径中的引号
    pdf_file = pdf_file.strip('"\'')
    
    # 统一路径分隔符
    pdf_file = os.path.normpath(pdf_file)
    
    # 检查文件是否存在
    if not os.path.exists(pdf_file):
        print('错误：文件不存在！')
    else:
        # 执行转换
        convert_pdf_to_word(pdf_file)