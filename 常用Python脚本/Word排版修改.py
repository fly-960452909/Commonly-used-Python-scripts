from docx import Document
import os
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def modify_word_layout(input_file, output_file, font_name='宋体', font_size=12, 
                     left_margin=1.0, right_margin=1.0, 
                     top_margin=1.0, bottom_margin=1.0,
                     indent_first_line=False, indent_spaces=2,
                     remove_special_chars=False):
    """
    修改Word文档排版
    :param input_file: 输入Word文件路径
    :param output_file: 输出Word文件路径
    :param font_name: 字体名称，默认为宋体
    :param font_size: 字号大小，默认为12
    :param left_margin: 左边距(英寸)，默认为1.0
    :param right_margin: 右边距(英寸)，默认为1.0
    :param top_margin: 上边距(英寸)，默认为1.0
    :param bottom_margin: 下边距(英寸)，默认为1.0
    :param indent_first_line: 是否首行缩进，默认为False
    :param indent_spaces: 缩进空格数，默认为2
    :param remove_special_chars: 是否去除特殊符号(#、*、-)，默认为False
    """
    # 打开文档
    doc = Document(input_file)
    
    # 设置全局样式
    style = doc.styles['Normal']
    font = style.font
    font.name = font_name
    font.size = Pt(font_size)
    
    # 设置页边距
    for section in doc.sections:
        section.left_margin = Inches(left_margin)
        section.right_margin = Inches(right_margin)
        section.top_margin = Inches(top_margin)
        section.bottom_margin = Inches(bottom_margin)
    
    # 修改每个段落的格式
    for paragraph in doc.paragraphs:
        if remove_special_chars:
            # 去除特殊符号
            text = paragraph.text
            text = text.replace('#', '').replace('*', '').replace('-', '')
            paragraph.text = text
            
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.line_spacing = 1.5
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        if indent_first_line:
             # 每个空格约等于0.25厘米
             paragraph.paragraph_format.first_line_indent = Inches(indent_spaces * 0.25 / 2.54)
    
    # 保存修改后的文档
    doc.save(output_file)

if __name__ == '__main__':
    # 获取并处理输入路径
    input_file = input('请输入要修改的Word文件路径: ').strip().strip('"').strip("'")
    output_file = input('请输入修改后保存的文件路径: ').strip().strip('"').strip("'")
    
    # 统一路径分隔符并检查输入文件是否存在
    input_file = os.path.normpath(input_file)
    output_file = os.path.normpath(output_file)
    
    if not os.path.exists(input_file):
        print('错误：输入文件不存在！')
        exit(1)
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print('请设置排版参数(直接回车使用默认值):')
    font_name = input(f'字体名称(默认:宋体): ') or '宋体'
    font_size = int(input(f'字号大小(默认:12): ') or 12)
    left_margin = float(input(f'左边距(英寸)(默认:1.0): ') or 1.0)
    right_margin = float(input(f'右边距(英寸)(默认:1.0): ') or 1.0)
    top_margin = float(input(f'上边距(英寸)(默认:1.0): ') or 1.0)
    bottom_margin = float(input(f'下边距(英寸)(默认:1.0): ') or 1.0)
    indent_first_line = input(f'是否首行缩进(默认:否)[y/n]: ').lower() == 'y'
    indent_spaces = int(input(f'缩进空格数(默认:2): ') or 2)
    remove_special_chars = input(f'是否去除特殊符号(#、*、-)(默认:否)[y/n]: ').lower() == 'y'
    
    try:
        modify_word_layout(input_file, output_file, 
                          font_name=font_name, font_size=font_size,
                          left_margin=left_margin, right_margin=right_margin,
                          top_margin=top_margin, bottom_margin=bottom_margin,
                          indent_first_line=indent_first_line, indent_spaces=indent_spaces,
                          remove_special_chars=remove_special_chars)
        print('Word文档排版修改完成！')
    except Exception as e:
        print(f'处理文件时出错: {e}')
        print('请检查文件路径是否正确，以及文件是否为有效的Word文档')
    print('Word文档排版修改完成！')