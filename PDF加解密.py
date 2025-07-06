import PyPDF2
import os

# 加密PDF文件

def encrypt_pdf(input_pdf_path, output_pdf_path, password):
    try:
        # 打开PDF文件
        with open(input_pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            # 复制页面到新的PDF
            for page in reader.pages:
                writer.add_page(page)
            
            # 设置密码
            writer.encrypt(password)
            
            # 写入加密后的PDF
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
            print(f"PDF文件已加密并保存到: {output_pdf_path}")
    except Exception as e:
        print(f"加密失败: {str(e)}")

# 解密PDF文件

def decrypt_pdf(input_pdf_path, output_pdf_path, password):
    try:
        # 打开PDF文件
        with open(input_pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # 检查密码
            if reader.is_encrypted:
                reader.decrypt(password)
            
            writer = PyPDF2.PdfWriter()
            
            # 复制页面到新的PDF
            for page in reader.pages:
                writer.add_page(page)
            
            # 写入解密后的PDF
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
            print(f"PDF文件已解密并保存到: {output_pdf_path}")
    except Exception as e:
        print(f"解密失败: {str(e)}")

# 破解PDF文件

def crack_pdf(input_pdf_path, output_pdf_path, password_list=None, max_length=4):
    print("警告：破解加密PDF文件可能违反法律和道德规范，请确保您有合法权限！")
    try:
        if password_list:
            print("正在尝试字典攻击...")
            for password in password_list:
                try:
                    with open(input_pdf_path, 'rb') as file:
                        reader = PyPDF2.PdfReader(file)
                        if reader.is_encrypted:
                            if reader.decrypt(password):
                                print(f"成功破解！密码为: {password}")
                                decrypt_pdf(input_pdf_path, output_pdf_path, password)
                                return
                except:
                    continue
        else:
            print("正在尝试暴力破解...")
            from itertools import product
            import string
            
            # 提供更多字符集选项
            char_sets = {
                '1': string.digits,
                '2': string.ascii_lowercase,
                '3': string.ascii_uppercase,
                '4': string.ascii_letters,
                '5': string.ascii_letters + string.digits,
                '6': string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{};:,.<>?'
            }
            
            print("请选择字符集：")
            print("1. 仅数字 (0-9)")
            print("2. 仅小写字母 (a-z)")
            print("3. 仅大写字母 (A-Z)")
            print("4. 大小写字母 (a-z, A-Z)")
            print("5. 字母和数字 (a-z, A-Z, 0-9)")
            print("6. 全部可打印字符 (默认)")
            choice = input("输入选项(1-6，默认6): ").strip() or '6'
            chars = char_sets.get(choice, char_sets['6'])
            
            # 计算总尝试次数
            total_attempts = sum(len(chars)**length for length in range(1, max_length+1))
            current_attempt = 0
            last_progress = 0
            
            for length in range(1, max_length+1):
                for attempt in product(chars, repeat=length):
                    current_attempt += 1
                    password = ''.join(attempt)
                    
                    # 在特定进度点显示进度
                    progress = int((current_attempt / total_attempts) * 100)
                    progress_thresholds = [0, 1, 5, 10, 20, 30, 50, 70, 90, 100]
                    if progress in progress_thresholds and progress != last_progress:
                        print(f"破解进度: {progress}% (尝试次数: {current_attempt}/{total_attempts})")
                        last_progress = progress
                    
                    try:
                        with open(input_pdf_path, 'rb') as file:
                            reader = PyPDF2.PdfReader(file)
                            if reader.is_encrypted:
                                if reader.decrypt(password):
                                    print(f"成功破解！密码为: {password}")
                                    decrypt_pdf(input_pdf_path, output_pdf_path, password)
                                    return
                    except:
                        continue
        print("破解失败：无法找到正确密码")
    except Exception as e:
        print(f"破解过程中出错: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    action = input('请选择操作（加密/解密/破解）：').strip().lower()
    input_pdf = input('请输入PDF文件路径：').strip().strip('"\'')
    output_pdf = input('请输入输出PDF文件路径：').strip().strip('"\'')
    
    # 检查文件是否存在
    if not os.path.exists(input_pdf):
        print('错误：输入文件不存在！')
    else:
        # 执行加密、解密或破解
        if action == '加密':
            password = input('请输入密码：').strip()
            encrypt_pdf(input_pdf, output_pdf, password)
        elif action == '解密':
            password = input('请输入密码：').strip()
            decrypt_pdf(input_pdf, output_pdf, password)
        elif action == '破解':
            use_dict = input('是否使用字典文件？(y/n)：').strip().lower() == 'y'
            if use_dict:
                dict_path = input('请输入字典文件路径：').strip().strip('"\'')
                if os.path.exists(dict_path):
                    with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                        passwords = [line.strip() for line in f]
                    crack_pdf(input_pdf, output_pdf, passwords)
                else:
                    print('错误：字典文件不存在！')
            else:
                max_len = int(input('请输入最大密码长度(默认4)：') or '4')
                crack_pdf(input_pdf, output_pdf, max_length=max_len)
        else:
            print('错误：无效的操作选择！')