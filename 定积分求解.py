from sympy import symbols, integrate, init_printing
from sympy.abc import x
import matplotlib.pyplot as plt
from sympy import latex
import os

# 初始化漂亮的打印格式
init_printing(use_unicode=True)

def calculate_definite_integral():
    """
    计算用户输入的函数在指定区间的定积分
    """
    # 获取用户输入的数学表达式
    expression = input("请输入要求解定积分的函数表达式（使用x作为变量，例如：x**2 + 2*x + 1）：")
    
    # 获取积分下限
    lower_limit = input("请输入积分下限：")
    
    # 获取积分上限
    upper_limit = input("请输入积分上限：")
    
    try:
        # 计算定积分
        integral = integrate(expression, (x, lower_limit, upper_limit))
        
        # 输出结果
        print(f"\n定积分结果为：{integral}")
        
        # 渲染为数学公式图片
        plt.figure(figsize=(8, 2))
        plt.text(0.1, 0.5, f'$\int_{{{lower_limit}}}^{{{upper_limit}}} {latex(sympify(expression))}\,dx = {latex(integral)}$', fontsize=14)
        plt.axis('off')
        
        # 保存图片
        if not os.path.exists('output'):
            os.makedirs('output')
        img_path = os.path.join('output', 'definite_integral_result.png')
        plt.savefig(img_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"\n公式图片已保存到: {img_path}")
        
    except Exception as e:
        print(f"错误：无法计算积分 - {e}")
        print("请确保表达式格式正确并使用x作为变量，例如：sin(x), x**2 + 2*x + 1")

if __name__ == "__main__":
    calculate_definite_integral()