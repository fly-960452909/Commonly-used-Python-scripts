import os
from PIL import Image

# 图片合成

def composite_images(input_folder, output_image_path):
    try:
        # 获取所有图片文件
        images = [Image.open(os.path.join(input_folder, file)) for file in os.listdir(input_folder) if file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        # 确定合成图片的尺寸
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        
        # 创建新的空白图像
        composite_image = Image.new('RGB', (total_width, max_height))
        
        # 将每张图片粘贴到新图像上
        x_offset = 0
        for img in images:
            composite_image.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # 保存合成后的图片
        composite_image.save(output_image_path)
        print(f"Composite image saved as {output_image_path}")
    except Exception as e:
        print(f"合成失败: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    input_folder = input('请输入图片输入文件夹路径：').strip().strip('"\'')
    output_image_path = input('请输入输出图片路径：').strip().strip('"\'')
    
    # 检查文件夹是否存在
    if not os.path.exists(input_folder):
        print('错误：输入文件夹不存在！')
    else:
        # 执行图片合成
        composite_images(input_folder, output_image_path)