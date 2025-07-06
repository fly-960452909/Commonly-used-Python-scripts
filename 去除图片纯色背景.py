from PIL import Image, ImageSequence # 导入 ImageSequence
import os

# 修改函数签名，接收 output_path_base (不含扩展名)
def remove_solid_background(input_path, output_path_base, tolerance=30):
    """
    移除图片（包括静态图和动图GIF）的纯色背景。

    Args:
        input_path (str): 输入图片的路径。
        output_path_base (str): 输出图片的基础路径（不含扩展名）。
        tolerance (int): 颜色容差值，用于判断像素是否属于背景。
                         数值越大，越多相近的颜色会被当作背景移除。
    """
    try:
        img = Image.open(input_path)

        # 检查图片是否为动图 (is_animated 属性)
        if not getattr(img, "is_animated", False):
            # --- 处理静态图片 ---
            img = img.convert("RGBA")
            datas = img.getdata()

            if not datas:
                 print(f"错误：无法读取图片数据 {input_path}")
                 return

            newData = []
            background_color = datas[0] # 获取左上角像素颜色

            for item in datas:
                diff_r = abs(item[0] - background_color[0])
                diff_g = abs(item[1] - background_color[1])
                diff_b = abs(item[2] - background_color[2])
                if diff_r <= tolerance and diff_g <= tolerance and diff_b <= tolerance:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)

            img.putdata(newData)
            output_path = f"{output_path_base}_nobg.png" # 静态图输出为 PNG
            img.save(output_path, "PNG")
            print(f"静态图片背景已移除，图片已保存至: {output_path}")

        else:
            # --- 处理 GIF 动图 ---
            frames_processed = []
            durations = []
            loop_count = img.info.get('loop', 0) # 获取循环次数

            # 获取第一帧并确定背景色
            img.seek(0) # 定位到第一帧
            first_frame = img.copy().convert("RGBA")
            background_color = first_frame.getdata()[0]

            # 遍历所有帧
            for frame in ImageSequence.Iterator(img):
                durations.append(frame.info.get('duration', 100)) # 获取帧持续时间

                frame_rgba = frame.convert("RGBA")
                datas = frame_rgba.getdata()
                newData = []

                for item in datas:
                    # 使用第一帧的背景色进行比较
                    diff_r = abs(item[0] - background_color[0])
                    diff_g = abs(item[1] - background_color[1])
                    diff_b = abs(item[2] - background_color[2])
                    if diff_r <= tolerance and diff_g <= tolerance and diff_b <= tolerance:
                        newData.append((255, 255, 255, 0)) # 透明
                    else:
                        newData.append(item)

                processed_frame = Image.new("RGBA", frame_rgba.size)
                processed_frame.putdata(newData)
                frames_processed.append(processed_frame)

            # 保存处理后的 GIF
            if frames_processed:
                output_path = f"{output_path_base}_nobg.gif" # 动图输出为 GIF
                frames_processed[0].save(
                    output_path,
                    save_all=True,
                    append_images=frames_processed[1:],
                    duration=durations,
                    loop=loop_count,
                    disposal=2, # 使用背景色填充（现在是透明）
                    format="GIF"
                )
                print(f"动图背景已移除，图片已保存至: {output_path}")
            else:
                print("错误：未能处理动图的任何帧。")

    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_path}")
    except Exception as e:
        print(f"处理图片时发生错误: {e}")

if __name__ == "__main__":
    # 更新输入提示
    input_image_path = input("请输入要处理的图片路径 (支持静态图和GIF动图): ")
    input_image_path = input_image_path.strip().strip('"').strip("'")

    # 获取基础文件名，不包含扩展名
    file_name, file_extension = os.path.splitext(input_image_path)
    # output_image_path = f"{file_name}_nobg.png" # 不再在这里决定输出扩展名

    # 可选：让用户输入容差值
    tolerance_str = input("请输入颜色容差值 (决定背景去除范围，值越大去除越多，建议 10-50，直接回车使用默认值 30): ")
    try:
        tolerance_value = int(tolerance_str) if tolerance_str else 30
    except ValueError:
        print("无效的容差值，将使用默认值 30。")
        tolerance_value = 30

    # 调用函数，传递基础文件名
    remove_solid_background(input_image_path, file_name, tolerance_value)