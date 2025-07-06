from sympy import symbols, limit, init_printing, sympify
from sympy.abc import x
import matplotlib.pyplot as plt
from sympy import latex
import os

# 初始化漂亮的打印格式
init_printing(use_unicode=True)

def calculate_limit():
    """
    计算用户输入的函数在指定点的极限
    """
    # 获取用户输入的数学表达式
    expression = input("请输入要求解极限的函数表达式（使用x作为变量，例如：sin(x)/x）：")
    
    # 获取极限点
    limit_point = input("请输入极限点（例如：0, oo表示无穷大）：")
    
    # 获取极限方向（可选）
    direction = input("请输入极限方向（可选，+表示右极限，-表示左极限，留空表示双侧极限）：")
    
    try:
        # 处理无穷大符号
        if limit_point.lower() == 'oo':
            limit_point = 'oo'
        else:
            limit_point = float(limit_point)
            
        # 解析表达式确保运算优先级正确
        expr = sympify(expression)
        
        # 计算极限
        if direction == '+':
            result = limit(expr, x, limit_point, dir='+')
            print(f"\n右极限结果为：{result}")
        elif direction == '-':
            result = limit(expr, x, limit_point, dir='-')
            print(f"\n左极限结果为：{result}")
        else:
            result = limit(expr, x, limit_point)
            print(f"\n极限结果为：{result}")
        
        # 渲染为数学公式图片
        plt.figure(figsize=(8, 2))
        plt.text(0.1, 0.5, f'$\lim_{{x \to {limit_point}}} {latex(sympify(expression))} = {latex(result)}$', fontsize=14)
        plt.axis('off')
        
        # 保存图片
        if not os.path.exists('output'):
            os.makedirs('output')
        img_path = os.path.join('output', 'limit_result.png')
        plt.savefig(img_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"\n公式图片已保存到: {img_path}")
        
    except Exception as e:
        print(f"错误：无法计算极限 - {e}")
        print("请确保表达式格式正确并使用x作为变量，例如：sin(x)/x, (x**2 - 1)/(x - 1)")

if __name__ == "__main__":
    calculate_limit()