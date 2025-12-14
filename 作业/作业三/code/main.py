"""
作业三主程序
运行所有任务并生成结果
"""

import matplotlib.pyplot as plt
from pathlib import Path

def run_task1():
    """运行Task 1: Bezier曲线绘制圆"""
    print("="*60)
    print("Task 1: Bezier曲线绘制圆")
    print("="*60)
    
    import bezier_circle
    
    for num_seg in [4, 8]:
        print(f"\n生成 {num_seg} 段Bezier圆...")
        bezier_circle.visualize_bezier_circle(num_segments=num_seg)
    
    print("\n✓ Task 1 完成")


def run_task2():
    """运行Task 2: Loop细分算法"""
    print("\n" + "="*60)
    print("Task 2: Loop细分算法")
    print("="*60)
    
    from halfedge import TriangleMesh, load_obj, save_obj
    from loop_subdivision import subdivide_loop
    
    print("\n加载网格...")
    vertices, faces = load_obj('bunny.obj')
    print(f"原始网格: {len(vertices)} 顶点, {len(faces)} 面")
    
    print("\n构建半边结构...")
    mesh = TriangleMesh()
    mesh.build_from_obj(vertices, faces)
    
    # 保存原始网格
    original_faces = mesh.get_faces_indices()
    save_obj('bunny_original.obj', mesh.get_vertex_positions(), original_faces)
    print(f"保存原始网格: bunny_original.obj")
    
    # 执行Loop细分
    num_subdivisions = 2
    for i in range(num_subdivisions):
        print(f"\n执行第 {i+1} 次细分...")
        mesh = subdivide_loop(mesh)
        subdivided_faces = mesh.get_faces_indices()
        print(f"  细分后: {len(mesh.vertices)} 顶点, {len(subdivided_faces)} 面")
    
    # 保存细分后的网格
    final_faces = mesh.get_faces_indices()
    save_obj('bunny_subdivided.obj', mesh.get_vertex_positions(), final_faces)
    print(f"\n保存细分网格: bunny_subdivided.obj")
    
    print(f"\n统计信息:")
    print(f"  原始: {len(original_faces)} 面")
    print(f"  细分后: {len(final_faces)} 面")
    print(f"  增长倍数: {len(final_faces) / len(original_faces):.2f}x")
    
    print("\n✓ Task 2 完成")


def main():
    """主函数"""
    
    # 运行任务
    run_task1()
    run_task2()
   

if __name__ == '__main__':
    main()
