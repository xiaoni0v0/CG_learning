import numpy as np

from halfedge import TriangleMesh, Vertex, HalfEdge, load_obj, save_obj


def compute_old_vertex_position(
    old_mesh: "TriangleMesh", old_vertex: "Vertex"
) -> np.ndarray:
    """
    Args:
        old_mesh: 半边结构的三角网格
        old_vertex: Vertex对象

    Returns:
        numpy array: 新位置坐标


    提示：
        1. 使用 TriangleMesh类的get_vertex_one_ring_neighbors(old_vertex) 获取邻居顶点列表
        2. 计算邻居数量 n = len(neighbors)
        3. 根据n的值计算权重u
        4. 应用Loop计算公式
    """

    neighbor_position = old_mesh.get_vertex_one_ring_neighbors(old_vertex)
    n = len(neighbor_position)
    u = 3 / 16 if n == 3 else 3 / (8 * n)

    return (1 - n * u) * old_vertex.position + u * sum(
        x.position for x in neighbor_position
    )


def compute_edge_midpoint_position(halfedge: "HalfEdge") -> np.ndarray:
    """
    Args:
        halfedge: HalfEdge对象

    Returns:
        numpy array: 中点位置坐标

    提示：
        1. 获取边的起点和终点
        2. 获取边对应的两个对立点
        3. 应用Loop计算公式
    """

    A, B = halfedge.vertex.position, halfedge.twin.vertex.position
    C, D = halfedge.next.vertex.position, halfedge.twin.next.vertex.position

    return 3 / 8 * (A + B) + 1 / 8 * (C + D)


def subdivide_loop(old_mesh: "TriangleMesh"):
    """
    Loop细分算法
    """
    new_mesh = TriangleMesh()

    # 步骤1：复制旧顶点并更新位置
    old_to_new_vertex = {}
    for old_v in old_mesh.vertices:
        new_pos = compute_old_vertex_position(old_mesh, old_v)
        new_v = Vertex(new_pos)
        old_to_new_vertex[id(old_v)] = new_v
        new_mesh.vertices.append(new_v)

    # 步骤2：预计算所有边的中点位置
    halfedge_to_midpoint = {}

    for he in old_mesh.halfedges:
        # 只处理每条边一次
        if he.twin is not None and id(he.twin) in halfedge_to_midpoint:
            halfedge_to_midpoint[id(he)] = halfedge_to_midpoint[id(he.twin)]
        else:
            mid_pos = compute_edge_midpoint_position(he)
            mid_vertex = Vertex(mid_pos)
            new_mesh.vertices.append(mid_vertex)
            halfedge_to_midpoint[id(he)] = mid_vertex

    # 步骤3：遍历所有面进行分裂
    for old_face in old_mesh.faces:
        # 获取旧面的三条半边
        he0 = old_face.halfedge
        he1 = he0.next
        he2 = he1.next

        # 获取旧面的三个顶点
        # he0 指向 v0, he1 指向 v1, he2 指向 v2
        old_v0 = he0.vertex
        old_v1 = he1.vertex
        old_v2 = he2.vertex

        # 映射到新网格
        new_v0 = old_to_new_vertex[id(old_v0)]
        new_v1 = old_to_new_vertex[id(old_v1)]
        new_v2 = old_to_new_vertex[id(old_v2)]

        # 获取三条边的中点
        # he0: v2->v0, he1: v0->v1, he2: v1->v2
        m0 = halfedge_to_midpoint[id(he0)]  # v2->v0 的中点
        m1 = halfedge_to_midpoint[id(he1)]  # v0->v1 的中点
        m2 = halfedge_to_midpoint[id(he2)]  # v1->v2 的中点

        # 创建4个新三角形
        # 原始三角形的三个角
        new_mesh.create_triangle(new_v0, m1, m0)
        new_mesh.create_triangle(new_v1, m2, m1)
        new_mesh.create_triangle(new_v2, m0, m2)
        # 中心三角形
        new_mesh.create_triangle(m0, m1, m2)

    # 步骤4：重建twin关系
    new_mesh.rebuild_twins()

    return new_mesh


def main():
    print("Loading mesh...")
    vertices, faces = load_obj("bunny.obj")
    print(f"Loaded {len(vertices)} vertices, {len(faces)} faces")

    print("Building halfedge structure...")
    mesh = TriangleMesh()
    mesh.build_from_obj(vertices, faces)

    original_faces = mesh.get_faces_indices()
    save_obj("bunny_original.obj", mesh.get_vertex_positions(), original_faces)
    print(f"Saved bunny_original.obj with {len(original_faces)} faces")

    # 执行Loop细分
    for i in range(2):
        print(f"\nPerforming Loop subdivision round {i+1}...")
        mesh = subdivide_loop(mesh)
        subdivided_faces = mesh.get_faces_indices()
        print(
            f"After subdivision {i+1}: {len(mesh.vertices)} vertices, {len(subdivided_faces)} faces"
        )

    final_faces = mesh.get_faces_indices()
    save_obj("bunny_subdivided.obj", mesh.get_vertex_positions(), final_faces)
    print(f"\nSaved bunny_subdivided.obj with {len(final_faces)} faces")
    print("Done!")


if __name__ == "__main__":
    main()
