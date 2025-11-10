"""
投影对比示例
展示透视投影和正交投影的区别
"""

import numpy as np

# 添加父目录到Python路径
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Triangle, Rasterization, LookAt, Perspective, Ortho


def projection_comparison_example():
    """透视投影和正交投影对比"""
    print("=== 透视投影和正交投影对比 ===")

    # 创建两个渲染器
    perspective_renderer = Rasterization(512, 512)
    ortho_renderer = Rasterization(512, 512)

    # 设置相同的视图矩阵
    view_matrix = LookAt(np.array([0, 0, 10]), np.array([0, 0, 0]), np.array([0, 1, 0]))
    perspective_renderer.setViewM(view_matrix)
    ortho_renderer.setViewM(view_matrix)

    # 设置不同的投影矩阵
    perspective_renderer.setProjM(Perspective(45, 1.0, 0.1, 50.0))
    ortho_renderer.setProjM(Ortho(-3, 3, -3, 3, 0.1, 50.0))

    # 创建两个三角形（一近一远）
    triangles = []

    # 近三角形（红色）
    t1 = Triangle()
    t1.setVertex(0, 0, 0, 0)
    t1.setVertex(1, -1, 1, 0)
    t1.setVertex(2, -2, 0, 0)
    t1.setColor(0, 1.0, 0.0, 0.0)
    t1.setColor(1, 1.0, 0.0, 0.0)
    t1.setColor(2, 1.0, 0.0, 0.0)

    # 远三角形（绿色）
    t2 = Triangle()
    t2.setVertex(0, 0, 0, -5)
    t2.setVertex(1, 2, 0, -5)
    t2.setVertex(2, 1, 1, -5)
    t2.setColor(0, 0.0, 1.0, 0.0)
    t2.setColor(1, 0.0, 1.0, 0.0)
    t2.setColor(2, 0.0, 1.0, 0.0)

    triangles = [t1, t2]

    # 渲染
    perspective_renderer.render(triangles)
    ortho_renderer.render(triangles)

    perspective_renderer.save_image("perspective_projection.png")
    ortho_renderer.save_image("orthographic_projection.png")

    print("投影对比完成")


if __name__ == "__main__":
    projection_comparison_example()
