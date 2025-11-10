"""
用于清理（删除）渲染出的图像
"""

import os

PATH = [
    ["./orthographic_projection.png", "./perspective_projection.png"],
    ["./basic_triangle.png"],
    [f"./triangle_rotated_{i}.png" for i in (45, 90, 135, 180)],
    [f"./rotation_slerp_t_{i:0.2f}.png" for i in (0.0, 0.25, 0.5, 0.75, 1.0)],
    ["./depth_test_disabled.png", "./depth_test_enabled.png"],
    ["./thin_triangles_aliasing.png", "./thin_triangles_antialiasing.png"],
]


def clean_all():
    for row in PATH:
        for file in row:
            if os.path.exists(file):
                os.remove(file)
                print(f"文件 {file} 已删除")
            else:
                # print(f'文件 {file} 不存在')
                pass


if __name__ == "__main__":
    clean_all()
