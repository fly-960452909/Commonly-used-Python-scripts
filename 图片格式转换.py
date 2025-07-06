import os
from PIL import Image

# 图片格式转换

def convert_image_format(input_folder, output_folder, target_format):
    try:
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 遍历输入文件夹中的所有图片
        for filename in os.listdir(input_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(input_folder, filename)
                image = Image.open(image_path)
                
                # 转换格式
                base_filename = os.path.splitext(filename)[0]
                output_path = os.path.join(output_folder, f"{base_filename}.{target_format}")
                image.save(output_path, format=target_format.upper())
                print(f"Converted image saved as {output_path}")
    except Exception as e:
        print(f"格式转换失败: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    input_folder = input('请输入图片输入文件夹路径：').strip().strip('"\'')
    output_folder = input('请输入图片输出文件夹路径：').strip().strip('"\'')
    target_format = input('请输入目标格式（png/jpg/jpeg/bmp/gif）：').strip().lower()
    
    # 检查文件夹是否存在
    if not os.path.exists(input_folder):
        print('错误：输入文件夹不存在！')
    else:
        # 执行格式转换
        convert_image_format(input_folder, output_folder, target_format)