import os
import argparse
from PyPDF2 import PdfMerger

def merge_pdfs(input_files, output_file):
    merger = PdfMerger()
    
    for pdf in input_files:
        if os.path.exists(pdf):
            merger.append(pdf)
        else:
            print(f"文件 {pdf} 不存在，已跳过")
    
    merger.write(output_file)
    merger.close()
    print(f"PDF文件已合并为: {output_file}")

def get_pdf_files_from_folder(folder_path, sort_method='name'):
    """获取指定文件夹中所有的PDF文件"""
    pdf_files = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        
        # 根据不同的排序方法对文件进行排序
        if sort_method == 'name':
            files.sort()  # 按文件名字母顺序排序
        elif sort_method == 'name_natural':
            import re
            # 自然排序（如：1.pdf, 2.pdf, 10.pdf 而不是 1.pdf, 10.pdf, 2.pdf）
            files.sort(key=lambda f: [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', f)])
        elif sort_method == 'date':
            # 按文件修改日期排序
            files.sort(key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
        elif sort_method == 'size':
            # 按文件大小排序
            files.sort(key=lambda f: os.path.getsize(os.path.join(folder_path, f)))
        
        for file in files:
            pdf_files.append(os.path.join(folder_path, file))
        
        if pdf_files:
            print(f"找到 {len(pdf_files)} 个PDF文件")
        else:
            print(f"在文件夹 {folder_path} 中没有找到PDF文件")
    else:
        print(f"文件夹 {folder_path} 不存在或不是一个有效的目录")
    return pdf_files

# 使用示例
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='合并PDF文件')
    parser.add_argument('-f', '--folder', help='包含PDF文件的文件夹路径')
    parser.add_argument('-o', '--output', help='输出的PDF文件名')
    parser.add_argument('-i', '--input', nargs='+', help='要合并的PDF文件列表')
    parser.add_argument('-s', '--sort', choices=['name', 'name_natural', 'date', 'size'], 
                        default='name', help='PDF文件排序方式: name(字母顺序), name_natural(自然排序), date(修改日期), size(文件大小)')
    parser.add_argument('-m', '--manual', action='store_true', help='手动指定PDF文件合并顺序')
    args = parser.parse_args()
    
    # 如果没有通过命令行参数输入，则交互式输入
    if not args.folder:
        args.folder = input("请输入包含PDF文件的文件夹路径：").strip('"\'')  # 去除可能输入的引号
    if not args.output:
        args.output = input("请输入输出的PDF文件名（含完整路径）：").strip('"\'')  # 去除可能输入的引号
    
    # 询问排序方式
    if not args.sort:
        print("\n请选择PDF文件排序方式:")
        print("1. 按文件名字母顺序排序 (name)")
        print("2. 按文件名自然排序 (name_natural)")
        print("3. 按文件修改日期排序 (date)")
        print("4. 按文件大小排序 (size)")
        sort_choice = input("请输入选择 (1-4，默认为1): ").strip()
        sort_methods = {
            '1': 'name',
            '2': 'name_natural',
            '3': 'date',
            '4': 'size'
        }
        args.sort = sort_methods.get(sort_choice, 'name')
    
    if args.folder:
        # 从文件夹获取PDF文件
        pdfs_to_merge = get_pdf_files_from_folder(args.folder, args.sort)
        
        # 如果选择手动排序
        if args.manual or input("\n是否需要手动调整合并顺序？(y/n，默认n): ").lower().strip() == 'y':
            print("\n当前文件顺序:")
            for i, pdf in enumerate(pdfs_to_merge):
                print(f"{i+1}. {os.path.basename(pdf)}")
            
            print("\n请输入新的文件顺序 (输入文件编号，用空格分隔，如: 3 1 2)")
            try:
                new_order = [int(x)-1 for x in input().split()]
                if all(0 <= i < len(pdfs_to_merge) for i in new_order):
                    pdfs_to_merge = [pdfs_to_merge[i] for i in new_order]
                    print("文件顺序已更新")
                else:
                    print("输入的编号无效，将使用原顺序")
            except:
                print("输入格式错误，将使用原顺序")
    elif args.input:
        # 使用指定的PDF文件列表
        pdfs_to_merge = args.input
    else:
        # 默认示例
        pdfs_to_merge = [
            "文件1.pdf",
            "文件2.pdf",
            "文件3.pdf"
        ]
        print("使用默认PDF文件列表。使用 -f 参数指定文件夹或 -i 参数指定文件列表。")
    
    # 输出的合并后PDF文件名
    output = args.output
    
    if pdfs_to_merge:
        # 确保输出目录存在
        output_dir = os.path.dirname(output)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"已创建输出目录: {output_dir}")
        
        merge_pdfs(pdfs_to_merge, output)
        print(f"\n合并完成! 文件已保存到: {output}")
    else:
        print("没有找到要合并的PDF文件")