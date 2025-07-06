import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from numpy import sin, cos, tan, log, log10, exp, sqrt, pi, e

def plot_implicit_function():
    """
    绘制隐式函数图像
    """
    # 获取用户输入的隐式方程
    equation_input = input("请输入隐式方程（使用x和y作为变量，例如：x^2 + y^2 = 1）：")
    
    try:
        # 处理等式输入，转换为表达式形式
        if '=' in equation_input:
            equation = equation_input.split('=')[0].strip() + '-' + equation_input.split('=')[1].strip()
        else:
            equation = equation_input
            
        # 替换^为**以支持幂运算
        equation = equation.replace('^', '**')
        
        # 创建网格
        x = np.linspace(-10, 10, 400)
        y = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x, y)
        
        # 计算方程值
        Z = eval(equation, {'x': X, 'y': Y, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 
                          'log': np.log, 'log10': np.log10, 'exp': np.exp, 
                          'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e})
        
        # 创建图形
        plt.figure(figsize=(8, 6))
        
        # 绘制等高线图（Z=0）
        plt.contour(X, Y, Z, [0], colors='b', linewidths=2)
        
        # 添加坐标轴
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        
        # 添加网格
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # 添加标题
        plt.title(f'隐式函数图像: {equation}=0')
        plt.xlabel('x轴')
        plt.ylabel('y轴')
        
        # 显示图形
        plt.show()
        
    except Exception as e:
        print(f"错误：无法解析方程 - {e}\n请确保方程格式正确并使用x和y作为变量，例如：x**2 + y**2 - 1")
        print("支持以下数学函数：sin, cos, tan, log, log10, exp, sqrt, pi, e")

def plot_function():
    """
    绘制用户输入的数学函数图像
    """
    # 获取用户输入的数学表达式
    expression = input("请输入数学表达式（使用x作为变量，例如：x**2 + 2*x + 1 或 y=x**2）：")
    
    # 处理'y='开头的表达式
    if expression.startswith('y='):
        expression = expression[2:].strip()
    
    try:
        # 定义x的范围
        x = np.linspace(-10, 10, 400)
        
        # 计算y值
        y = eval(expression, {'x': x, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 'log': np.log, 'log10': np.log10, 'exp': np.exp, 'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e})
        
        # 创建图形
        plt.figure(figsize=(8, 6))
        
        # 绘制函数曲线
        plt.plot(x, y, 'b-', linewidth=2, label=f'$y = {latex(sympify(expression))}$')
        
        # 添加坐标轴
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        
        # 添加网格
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # 添加图例和标题
        plt.legend()
        plt.title('笛卡尔坐标系函数图像')
        plt.xlabel('x轴')
        plt.ylabel('y轴')
        
        # 显示图形
        plt.show()
        
    except Exception as e:
        print(f"错误：无法解析表达式 - {e}\n请确保表达式格式正确并使用x作为变量，例如：sin(x), x**2 + 2*x + 1 或 y=x**2")
        print("支持以下数学函数：sin, cos, tan, log, log10, exp, sqrt, pi, e")

def plot_3d_function():
    """
    绘制三维函数图像 z = f(x,y)
    """
    # 获取用户输入的数学表达式
    expression = input("请输入三维数学表达式（使用x和y作为变量，例如：x**2 + y**2 或 z=x**2 + y**2）：")
    
    # 处理'z='开头的表达式
    if expression.startswith('z='):
        expression = expression[2:].strip()
    
    try:
        # 定义x和y的范围
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)
        
        # 计算z值
        Z = eval(expression, {'x': X, 'y': Y, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 
                            'log': np.log, 'log10': np.log10, 'exp': np.exp, 
                            'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e})
        
        # 创建3D图形
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制曲面
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
        
        # 添加颜色条
        fig.colorbar(surf, shrink=0.5, aspect=5)
        
        # 添加标题和标签
        ax.set_title(f'三维函数图像: $z = {latex(sympify(expression))}$')
        ax.set_xlabel('x轴')
        ax.set_ylabel('y轴')
        ax.set_zlabel('z轴')
        
        # 显示图形
        plt.show()
        
    except Exception as e:
        print(f"错误：无法解析表达式 - {e}\n请确保表达式格式正确并使用x和y作为变量，例如：sin(x)+cos(y), x**2 + y**2 或 z=x**2 + y**2")
        print("支持以下数学函数：sin, cos, tan, log, log10, exp, sqrt, pi, e")

if __name__ == "__main__":
    print("请选择绘图类型：")
    print("1. 显式函数 y = f(x)")
    print("2. 隐式方程 f(x,y) = 0")
    print("3. 三维函数 z = f(x,y)")
    choice = input("请输入选项(1,2或3): ")
    
    if choice == "1":
        plot_function()
    elif choice == "2":
        plot_implicit_function()
    elif choice == "3":
        plot_3d_function()
    else:
        print("无效选项，默认绘制显式函数")
        plot_function()