import math
import os
import comtypes.client
from PIL import Image

def ppt_to_pdf(input_ppt, output_pdf, slides_per_page=(2,2)):
    # 直接在输入文件所在目录创建临时文件夹
    temp_dir = os.path.join(os.path.dirname(input_ppt), "temp_ppt_images")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # 转换PPT为图片
        images = convert_ppt_to_images(input_ppt, temp_dir)
        
        # 拼接图片生成PDF
        create_pdf_from_images(images, output_pdf, slides_per_page, margin=50, spacing=20)
        
    finally:
        # 清理临时文件
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

def convert_ppt_to_images(ppt_path, output_dir):
    import win32con
    import win32gui
    import time
    powerpoint = None
    presentation = None
    try:
        powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
        powerpoint.Visible = 1
        powerpoint.WindowState = 2
        
        # 新增窗口检测循环
        start_time = time.time()
        hwnd = 0
        while time.time() - start_time < 10:  # 10秒超时
            hwnd = win32gui.FindWindow(None, "Microsoft PowerPoint")
            if hwnd != 0:
                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0, win32con.SWP_HIDEWINDOW)
                break
            time.sleep(0.5)
        presentation = powerpoint.Presentations.Open(
            os.path.abspath(ppt_path),
            WithWindow=False,
            Untitled=0
        )
        slides_count = presentation.Slides.Count
        
        images = []
        for i in range(1, slides_count + 1):
            try:
                # 添加对象有效性检查
                if not presentation or presentation.Application is None:
                    raise RuntimeError("Presentation对象已失效")
                    
                slide = presentation.Slides.Item(i)  # 改用Item方法获取幻灯片
                export_path = os.path.join(output_dir, f"slide_{i}.png")
                
                # 添加重试机制
                for attempt in range(3):
                    try:
                        slide.Export(export_path, "PNG", 700)
                        images.append(export_path)
                        break
                    except Exception as e:
                        if attempt == 2:
                            raise
                        time.sleep(1)
            except Exception as e:
                print(f"转换第 {i} 页失败: {str(e)}")
                continue
        return images
    finally:
        # 增加gc模块导入
        import gc
        # 增加资源释放力度
        try:
            if presentation:
                presentation.Close()
                presentation = None
        except:
            pass
        try:
            if powerpoint:
                powerpoint.Quit()
                powerpoint = None
        except:
            pass
        time.sleep(8)  # 延长关闭等待时间
        gc.collect()
        # 强制终止进程
        os.system(f"taskkill /f /im POWERPNT.EXE")

def create_pdf_from_images(image_paths, output_pdf, grid_size, margin=50, spacing=20):
    rows, cols = grid_size
    images = [Image.open(img) for img in image_paths]
    
    # 计算单个幻灯片尺寸（考虑边距和间距）
    base_width = images[0].width
    base_height = images[0].height
    
    # 计算可用空间
    usable_width = base_width * cols + spacing * (cols - 1)
    usable_height = base_height * rows + spacing * (rows - 1)
    
    # 创建带边距的PDF页面
    pdf_page_width = usable_width + margin*2
    pdf_page_height = usable_height + margin*2
    
    pdf_images = []
    
    for i in range(0, len(images), rows*cols):
        page_images = images[i:i+rows*cols]
        pdf_page = Image.new('RGB', (pdf_page_width, pdf_page_height), (255, 255, 255))
        
        for idx, img in enumerate(page_images):
            row = idx // cols
            col = idx % cols
            
            # 计算带边距和间距的位置
            x = margin + col * (base_width + spacing)
            y = margin + row * (base_height + spacing)
            
            pdf_page.paste(img.resize((base_width, base_height), Image.Resampling.LANCZOS), (x, y))
        
        pdf_images.append(pdf_page)
    
    pdf_images[0].save(
        output_pdf, save_all=True, append_images=pdf_images[1:],
        resolution=700, quality=100
    )

def process_ppt_files(input_path):
    """处理输入路径（文件或文件夹）"""
    if os.path.isfile(input_path):
        return [input_path]
    
    ppt_files = []
    for file in os.listdir(input_path):
        if file.lower().endswith(('.ppt', '.pptx')):
            ppt_files.append(os.path.join(input_path, file))
    
    # 显示可选择的文件列表
    print("\n发现以下PPT文件：")
    for idx, file in enumerate(ppt_files, 1):
        print(f"{idx}. {os.path.basename(file)}")
    
    # 获取用户选择
    selections = input("请输入要合并的文件编号（用逗号分隔，例如1,3,5）: ").split(',')
    selected_files = []
    for s in selections:
        try:
            index = int(s.strip()) - 1
            if 0 <= index < len(ppt_files):
                selected_files.append(ppt_files[index])
        except ValueError:
            continue
    
    # 按选择顺序返回文件
    return selected_files

def merge_ppt_images(selected_files, temp_dir):
    """合并多个PPT的图片"""
    all_images = []
    for idx, ppt_file in enumerate(selected_files, 1):
        # 为每个PPT创建独立临时目录
        ppt_temp_dir = os.path.join(temp_dir, f"ppt_{idx}")
        os.makedirs(ppt_temp_dir, exist_ok=True)
        
        print(f"\n正在处理第 {idx}/{len(selected_files)} 个文件：{os.path.basename(ppt_file)}")
        images = convert_ppt_to_images(ppt_file, ppt_temp_dir)  # 传入独立目录
        all_images.extend(images)
    return all_images

if __name__ == "__main__":
    # 修改后的主程序逻辑
    input_path = input("请输入PPT文件或文件夹路径: ").strip().strip('"').strip("'")
    
    # 处理输入路径
    selected_files = process_ppt_files(input_path)
    if not selected_files:
        print("未找到有效的PPT文件")
        exit()
    
    # 创建临时文件夹（使用第一个文件的目录）
    temp_dir = os.path.join(os.path.dirname(selected_files[0]), "temp_ppt_images")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # 合并所有图片
        all_images = merge_ppt_images(selected_files, temp_dir)
        
        # 生成输出路径
        base_dir = os.path.dirname(selected_files[0])
        output_pdf = os.path.join(base_dir, "merged_combined.pdf")
        
        # 获取排列设置
        rows = int(input("请输入每页行数（默认2）: ") or 2)
        cols = int(input("请输入每页列数（默认2）: ") or 2)
        
        # 生成PDF
        create_pdf_from_images(all_images, output_pdf, (rows, cols), margin=50, spacing=20)
        print(f"\n合并完成！PDF已生成：{output_pdf}")
    
    finally:
        # 递归清理临时文件（修复目录删除问题）
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)