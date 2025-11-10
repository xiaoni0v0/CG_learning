"""
主程序入口
运行所有示例
"""

import time

from clean import clean_all
from examples import (
    basic_triangle_example,
    projection_comparison_example,
    antialiasing_comparison_example,
    depth_test_example,
    rotation_interpolation_example,
)

CLEAN = False


def main():
    """运行所有示例"""

    if CLEAN:
        clean_all()

    print("=" * 50)
    print("计算机图形学作业一：三角形光栅化")
    print("=" * 50)

    try:
        t0 = time.time()

        # 1. 基础渲染
        basic_triangle_example()
        print()

        # 2. 投影对比
        projection_comparison_example()
        print()

        # 3. 旋转插值
        rotation_interpolation_example()
        print()

        # 4. 深度测试
        depth_test_example()
        print()

        # 5. 抗锯齿对比（重点）
        antialiasing_comparison_example()
        print()

        print("=" * 50)
        print("所有示例已完成！")
        print("=" * 50)
        print("生成的图像文件:")
        print("- perspective_projection.png (透视投影)")
        print("- orthographic_projection.png (正交投影)")
        print("- basic_triangle.png (基础三角形)")
        print("- triangle_rotated_*.png (旋转三角形)")
        print("- rotation_slerp_*.png (四元数插值)")
        print("- depth_test.png (深度测试)")
        print("- thin_triangles_aliasing.png (走样效果) ")
        print("- thin_triangles_antialiasing.png (反走样效果)")
        print()

        print(f"运行耗时: {time.time() - t0:.2f}s")
        print()

    except Exception as e:
        print(f"运行出错: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
