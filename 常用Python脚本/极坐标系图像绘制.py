import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan, log, log10, exp, sqrt, pi, e

def plot_polar_function():
    """
    绘制极坐标函数图像 r = f(θ)
    """
    # 获取用户输入的数学表达式
    expression = input("请输入极坐标表达式（使用theta作为变量，例如：sin(2*theta) 或 r=sin(2*theta)）：")
    
    # 处理'r='开头的表达式
    if expression.startswith('r='):
        expression = expression[2:].strip()
    
    try:
        # 定义theta的范围
        theta = np.linspace(0, 2*np.pi, 1000)
        
        # 计算r值
        r = eval(expression, {'theta': theta, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 
                             'log': np.log, 'log10': np.log10, 'exp': np.exp, 
                             'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e})
        
        # 创建极坐标图形
        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, projection='polar')
        
        # 绘制极坐标曲线
        ax.plot(theta, r, 'b-', linewidth=2, label=f'r = {expression}')
        
        # 添加网格
        ax.grid(True)
        
        # 添加图例和标题
        plt.legend(loc='upper right')
        plt.title('极坐标系函数图像')
        
        # 显示图形
        plt.show()
        
    except Exception as e:
        print(f"错误：无法解析表达式 - {e}\n请确保表达式格式正确并使用theta作为变量，例如：sin(2*theta), cos(3*theta) 或 r=sin(2*theta)")
        print("支持以下数学函数：sin, cos, tan, log, log10, exp, sqrt, pi, e")

if __name__ == "__main__":
    plot_polar_function()