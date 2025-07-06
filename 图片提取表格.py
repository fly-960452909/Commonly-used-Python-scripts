import cv2
import pytesseract
import pandas as pd
from openpyxl import Workbook

# 配置Tesseract路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 读取图像
image_path = input('请输入图像文件路径：').strip().strip('"').strip("'")
image = cv2.imread(image_path)

# 转换为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用OCR提取文本
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(gray, config=custom_config)

# 将文本转换为DataFrame
lines = text.split('\n')
data = [line.split() for line in lines if line.strip()]
df = pd.DataFrame(data)

# 保存到Excel
excel_path = 'output.xlsx'
with pd.ExcelWriter(excel_path) as writer:
    df.to_excel(writer, sheet_name='提取数据', index=False)

print(f'表格已提取并保存到Excel：{excel_path}')