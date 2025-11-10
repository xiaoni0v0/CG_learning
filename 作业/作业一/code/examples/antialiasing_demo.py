"""
抗锯齿示例
展示走样和反走样效果对比
"""

import os
import sys

import numpy as np

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (
    Rasterization,
    LookAt,
    Perspective,
    create_jagged_triangle,
    create_thin_triangles,
)


def antialiasing_comparison_example():
    """抗锯齿对比示例"""
    print("=== 抗锯齿对比 ===")

    # 创建两个渲染器
    no_aa_renderer = Rasterization(512, 512)
    aa_renderer = Rasterization(512, 512)

    # 设置视图和投影矩阵
    view_matrix = LookAt(np.array([0, 0, 5]), np.array([0, 0, 0]), np.array([0, 1, 0]))
    proj_matrix = Perspective(45, 1.0, 0.1, 50.0)

    no_aa_renderer.setViewM(view_matrix)
    no_aa_renderer.setProjM(proj_matrix)

    aa_renderer.setViewM(view_matrix)
    aa_renderer.setProjM(proj_matrix)
    aa_renderer.enableAntialiasing(True)  # 启用抗锯齿

    # 创建细长三角形进行对比
    thin_triangles = create_thin_triangles()

    no_aa_renderer.clear_buffers()
    aa_renderer.clear_buffers()

    no_aa_renderer.render(thin_triangles)
    aa_renderer.render(thin_triangles)

    no_aa_renderer.save_image("thin_triangles_aliasing.png")
    aa_renderer.save_image("thin_triangles_antialiasing.png")

    print("抗锯齿对比完成")


if __name__ == "__main__":
    antialiasing_comparison_example()
