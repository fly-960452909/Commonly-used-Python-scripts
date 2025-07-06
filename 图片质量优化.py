import os
from PIL import Image, ImageEnhance

# 图片质量优化

def optimize_image_quality(input_folder, output_folder, brightness=1.0, contrast=1.0, saturation=1.0):
    try:
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 遍历输入文件夹中的所有图片
        for filename in os.listdir(input_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(input_folder, filename)
                image = Image.open(image_path)
                
                # 调整亮度
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(brightness)
                
                # 调整对比度
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(contrast)
                
                # 调整饱和度
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(saturation)
                
                # 保存优化后的图片
                output_path = os.path.join(output_folder, filename)
                image.save(output_path)
                print(f"Optimized image saved as {output_path}")
    except Exception as e:
        print(f"优化失败: {str(e)}")

if __name__ == '__main__':
    # 获取用户输入
    input_folder = input('请输入图片输入文件夹路径：').strip().strip('"\'')
    output_folder = input('请输入图片输出文件夹路径：').strip().strip('"\'')
    brightness = float(input('请输入亮度调整系数（默认1.0）：').strip())
    contrast = float(input('请输入对比度调整系数（默认1.0）：').strip())
    saturation = float(input('请输入饱和度调整系数（默认1.0）：').strip())
    
    # 检查文件夹是否存在
    if not os.path.exists(input_folder):
        print('错误：输入文件夹不存在！')
    else:
        # 执行优化
        optimize_image_quality(input_folder, output_folder, brightness, contrast, saturation)