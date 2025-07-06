import fitz  # PyMuPDF
import pandas as pd
import os

def pdf_to_excel(pdf_path, excel_path=None):
    """
    将PDF文件转换为Excel表格
    :param pdf_path: PDF文件路径
    :param excel_path: 输出的Excel文件路径（可选）
    :return: None
    """
    try:
        # 如果未指定输出路径，则使用原文件名，仅更改扩展名
        if excel_path is None:
            excel_path = os.path.splitext(pdf_path)[0] + '.xlsx'
        
        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)
        
        # 提取所有文本和表格数据
        all_text = []
        tables = []
        
        for page in pdf_document:
            # 提取文本
            text = page.get_text()
            if text.strip():
                all_text.append(text)
            
            # 提取表格
            table = page.find_tables()
            if table.tables:
                for t in table.tables:
                    tables.append(t.to_pandas())
        
        # 关闭PDF文件
        pdf_document.close()
        
        # 将数据写入Excel
        with pd.ExcelWriter(excel_path) as writer:
            # 合并所有文本为一个字符串
            combined_text = '\n\n'.join(all_text) if all_text else ''
            
            # 合并所有表格数据
            combined_tables = pd.concat(tables) if tables else pd.DataFrame()
            
            # 创建包含所有数据的工作表
            if combined_text or not combined_tables.empty:
                if not combined_tables.empty:
                    combined_tables.to_excel(writer, sheet_name='合并数据', index=False)
                    if combined_text:
                        # 在表格下方添加文本内容
                        ws = writer.sheets['合并数据']
                        ws.cell(row=len(combined_tables)+3, column=1, value='文本内容:')
                        ws.cell(row=len(combined_tables)+4, column=1, value=combined_text)
                else:
                    pd.DataFrame([combined_text], columns=['文本内容']).to_excel(writer, sheet_name='合并数据', index=False)
        
        print(f'转换成功！\nPDF文件：{pdf_path}\nExcel文件：{excel_path}')
        
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
        pdf_to_excel(pdf_file)