from sympy import symbols, integrate, init_printing
from sympy.abc import x
import matplotlib.pyplot as plt
from sympy import latex
import os

# 初始化漂亮的打印格式
init_printing(use_unicode=True)

def calculate_integral():
    """
    计算用户输入的函数的不定积分
    """
    # 获取用户输入的数学表达式
    expression = input("请输入要求解不定积分的函数表达式（使用x作为变量，例如：x**2 + 2*x + 1）：")
    
    try:
        # 计算不定积分
        integral = integrate(expression, x)
        
        # 输出结果
        print("\n不定积分结果为：")
        print(integral,end="")
        print("+C")
        
        # 渲染为数学公式图片
        plt.figure(figsize=(8, 2))
        plt.text(0.1, 0.5, f'$\int {latex(sympify(expression))}\,dx = {latex(integral)} + C$', fontsize=14)
        plt.axis('off')
        
        # 保存图片
        if not os.path.exists('output'):
            os.makedirs('output')
        img_path = os.path.join('output', 'integral_result.png')
        plt.savefig(img_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"\n公式图片已保存到: {img_path}")
        
    except Exception as e:
        print(f"错误：无法计算积分 - {e}")
        print("请确保表达式格式正确并使用x作为变量，例如：sin(x), x**2 + 2*x + 1")

if __name__ == "__main__":
    calculate_integral()