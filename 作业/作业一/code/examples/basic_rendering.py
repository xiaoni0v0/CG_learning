"""
基础渲染示例
包含基本三角形渲染和旋转
"""

import numpy as np
import copy

# 添加父目录到Python路径
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Triangle, Rasterization, LookAt, Perspective

def basic_triangle_example():
    """基本三角形渲染和旋转"""
    print("=== 基本三角形渲染和旋转 ===")
    
    renderer = Rasterization(512, 512)
    
    # 设置相机
    eye = np.array([0, 0, 5])
    center = np.array([0, 0, 0])
    up = np.array([0, 1, 0])
    
    view_matrix = LookAt(eye, center, up)
    renderer.setViewM(view_matrix)
    
    proj_matrix = Perspective(45, 1.0, 0.1, 50.0)
    renderer.setProjM(proj_matrix)
    
    # 创建三角形
    t = Triangle()
    t.setVertex(0, 0, 1.0, 0.0)
    t.setVertex(1, -1.0, -1.0, 0.0)
    t.setVertex(2, 1.0, -1.0, 0.0)
    
    t.setColor(0, 1.0, 0.0, 0.0)  # 红色
    t.setColor(1, 0.0, 1.0, 0.0)  # 绿色
    t.setColor(2, 0.0, 0.0, 1.0)  # 蓝色
    
    # 渲染基本三角形
    renderer.render([t])
    renderer.save_image("basic_triangle.png")
    
    # 演示旋转
    angles = [45, 90, 135, 180]
    for angle in angles:
        t_rotated = copy.deepcopy(t)
        t_rotated.rotate_norm(angle)
        
        renderer.clear_buffers()
        renderer.render([t_rotated])
        renderer.save_image(f"triangle_rotated_{angle}.png")
    
    print("基本三角形渲染完成")

if __name__ == "__main__":
    basic_triangle_example()
