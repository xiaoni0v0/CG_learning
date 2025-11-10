"""
旋转插值示例
使用四元数SLERP实现平滑旋转插值
"""

import numpy as np

# 添加父目录到Python路径
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Triangle, Rasterization, LookAt, Perspective, Quaternion

def interpolate_rotation_quaternion(t_value):
    """使用四元数SLERP进行旋转和颜色插值"""
    t_interp = Triangle()
    
    # 初始三角形顶点
    initial_vertices = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0]
    ])
    
    # 定义起始和结束四元数
    q_start = Quaternion(1.0, 0.0, 0.0, 0.0)
    
    # 结束：R = Rz(30°) * Ry(60°) * Rx(30°)
    rx = np.deg2rad(30)
    ry = np.deg2rad(60)
    rz = np.deg2rad(30)
    q_end = Quaternion.from_euler(rx, ry, rz)
    
    # 使用SLERP进行四元数插值
    q_current = Quaternion.slerp(q_start, q_end, t_value)
    
    # 转换为旋转矩阵
    rotation_matrix = q_current.to_rotation_matrix()
    
    # 应用旋转到顶点
    rotated_vertices = (rotation_matrix @ initial_vertices.T).T
    
    # 设置顶点
    for i in range(3):
        t_interp.setVertex(i, *rotated_vertices[i])
    
    # 插值颜色：从红色到绿色
    start_color = np.array([1.0, 0.0, 0.0])
    end_color = np.array([0.0, 1.0, 0.0])
    current_color = start_color * (1 - t_value) + end_color * t_value
    
    for i in range(3):
        t_interp.setColor(i, *current_color)
    
    return t_interp

def rotation_interpolation_example():
    """旋转插值示例"""
    print("=== 旋转插值（四元数SLERP） ===")
    
    renderer = Rasterization(512, 512)
    
    view_matrix = LookAt(np.array([0, 0, 5]), np.array([0, 0, 0]), np.array([0, 1, 0]))
    proj_matrix = Perspective(45, 1.0, 0.1, 50.0)
    
    renderer.setViewM(view_matrix)
    renderer.setProjM(proj_matrix)
    
    # 渲染关键帧
    t_values = [0, 0.25, 0.5, 0.75, 1.0]
    
    print("渲染旋转插值关键帧:")
    for t_val in t_values:
        print(f"  渲染 t = {t_val:.2f}")
        t_interp = interpolate_rotation_quaternion(t_val)
        
        renderer.clear_buffers()
        renderer.render([t_interp])
        renderer.save_image(f"rotation_slerp_t_{t_val:.2f}.png")
    
    print("旋转插值完成")

if __name__ == "__main__":
    rotation_interpolation_example()
