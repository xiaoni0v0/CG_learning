"""
深度测试示例
展示深度缓冲的作用
"""

import numpy as np
import sys
import os

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Triangle, Rasterization, LookAt, Perspective

def depth_test_example():
    """深度测试示例"""
    print("=== 深度测试对比 ===")
    
    # 创建两个渲染器：一个开启深度测试，一个关闭
    renderer_with_depth = Rasterization(512, 512)
    renderer_without_depth = Rasterization(512, 512)
    
    view_matrix = LookAt(np.array([0, 0, 5]), np.array([0, 0, 0]), np.array([0, 1, 0]))
    proj_matrix = Perspective(45, 1.0, 0.1, 50.0)
    
    # 设置相同的视图和投影矩阵
    renderer_with_depth.setViewM(view_matrix)
    renderer_with_depth.setProjM(proj_matrix)
    renderer_with_depth.enableDepthTest(True)  # 开启深度测试
    
    renderer_without_depth.setViewM(view_matrix)
    renderer_without_depth.setProjM(proj_matrix)
    renderer_without_depth.enableDepthTest(False)  # 关闭深度测试
    
    # 创建两个重叠的三角形来测试深度
    triangles = create_overlapping_triangles()
    
    # 渲染对比
    print("渲染开启深度测试的场景...")
    renderer_with_depth.render(triangles)
    renderer_with_depth.save_image("depth_test_enabled.png")
    
    print("渲染关闭深度测试的场景...")
    renderer_without_depth.render(triangles)
    renderer_without_depth.save_image("depth_test_disabled.png")
    
    print("深度测试对比完成")
    print("- depth_test_enabled.png: 开启深度测试（正确遮挡）")
    print("- depth_test_disabled.png: 关闭深度测试（按绘制顺序）")

def create_overlapping_triangles():
    """创建两个重叠的三角形用于深度测试"""
    triangles = []
    
    # 背景三角形（绿色，较远，z=-1）
    t1 = Triangle()
    t1.setVertex(0, 0, 1.2, -1)      # 顶点：上方
    t1.setVertex(1, -1.5, -1.2, -1)  # 左下
    t1.setVertex(2, 1.5, -1.2, -1)   # 右下
    t1.setColor(0, 0.0, 1.0, 0.0)    # 绿色
    t1.setColor(1, 0.0, 1.0, 0.0)
    t1.setColor(2, 0.0, 1.0, 0.0)
    
    # 前景三角形（红色，较近，z=0）
    t2 = Triangle()
    t2.setVertex(0, 0.5, -0.8, 0)    # 顶点：右下偏移
    t2.setVertex(1, -0.7, 0.8, 0)    # 左上
    t2.setVertex(2, 1.9, 0.8, 0)     # 右上
    t2.setColor(0, 1.0, 0.0, 0.0)    # 红色
    t2.setColor(1, 1.0, 0.0, 0.0)
    t2.setColor(2, 1.0, 0.0, 0.0)
    
    # 先添加远的三角形，再添加近的三角形
    # 这样在关闭深度测试时，近的会覆盖远的
    triangles.append(t2)  # 远的先绘制
    triangles.append(t1)  # 近的后绘制
    
    return triangles

if __name__ == "__main__":
    depth_test_example()
