import os
from PIL import Image

# 批量处理图片

def batch_process_images(input_folder, output_folder, operation):
    try:
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 遍历输入文件夹中的所有图片
        for filename in os.listdir(input_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(input_folder, filename)
                image = Image.open(image_path)
                
                # 执行指定操作
                if operation == '裁剪':
                    image = image.crop((0, 0, image.width // 2, image.height // 2))
                elif operation == '调整大小':
                    image = image.resize((image.width // 2, image.height // 2))
                elif operation == '旋转':
                    image = image.rotate(90)
                
                # 保存处理后的图片
                output_path = os.path.join(output_folder, filename)
                image.save(output_path)
                print(f"Processed image saved as {output_path}")
    except Exception as e:
        print(f"批量处理失败: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    input_folder = input('请输入图片输入文件夹路径：').strip().strip('"\'')
    output_folder = input('请输入图片输出文件夹路径：').strip().strip('"\'')
    operation = input('请选择操作（裁剪/调整大小/旋转）：').strip().lower()
    
    # 检查文件夹是否存在
    if not os.path.exists(input_folder):
        print('错误：输入文件夹不存在！')
    else:
        # 执行批量处理
        batch_process_images(input_folder, output_folder, operation)