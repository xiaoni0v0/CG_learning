import numpy as np

class HalfEdge:
    """半边数据结构 - 半边类"""
    
    def __init__(self):
        self.vertex = None      # 半边指向的顶点
        self.face = None        # 半边所属的面
        self.next = None        # 同一面内的下一条半边
        self.prev = None        # 同一面内的上一条半边
        self.twin = None        # 对应的反向半边


class Vertex:
    """半边数据结构 - 顶点类"""
    
    def __init__(self, position):
        self.position = np.array(position, dtype=float)
        self.halfedge = None    # 从该顶点出发的任意一条半边


class Face:
    """半边数据结构 - 面类"""
    
    def __init__(self):
        self.halfedge = None    # 面上的任意一条半边


class TriangleMesh:
    """半边数据结构网格"""
    
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.halfedges = []
    
    def build_from_obj(self, vertices, faces):
        """从顶点和面列表构建半边结构"""
        self.vertices = [Vertex(v) for v in vertices]
        
        edge_map = {}
        
        for face_indices in faces:
            face = Face()
            self.faces.append(face)
            
            halfedges_in_face = []
            for i in range(3):
                he = HalfEdge()
                self.halfedges.append(he)
                halfedges_in_face.append(he)
                
                # 半边 i 从顶点 i 指向顶点 (i+1)%3
                v_start = face_indices[i]
                v_end = face_indices[(i + 1) % 3]
                
                he.vertex = self.vertices[v_end]  # 半边指向终点
                self.vertices[v_end].halfedge = he
                he.face = face
                
                edge_map[(v_start, v_end)] = he
            
            for i in range(3):
                halfedges_in_face[i].next = halfedges_in_face[(i + 1) % 3]
                halfedges_in_face[i].prev = halfedges_in_face[(i - 1) % 3]
            
            face.halfedge = halfedges_in_face[0]
        
        # 建立twin关系
        for (v_start, v_end), he in edge_map.items():
            if (v_end, v_start) in edge_map:
                he.twin = edge_map[(v_end, v_start)]
    
    def rebuild_twins(self):
        """重建所有半边的twin关系"""
        # 清空所有twin
        for he in self.halfedges:
            he.twin = None
        
        # 建立边到半边的映射
        edge_map = {}
        for he in self.halfedges:
            # 半边从起点指向 he.vertex (终点)
            # 起点是 he.prev.vertex (因为 prev 指向起点)
            # 但在三角形中：he.prev.prev.vertex 才是起点
            # 让我们用正确的方式：通过遍历找起点
            
            # 对于三角形，如果 he 指向 v2，he.next 指向 v0，he.prev 指向 v1
            # 那么 he 是从 v1 指向 v2
            v_end = he.vertex
            v_start = he.prev.vertex if he.prev else None
            
            if v_start is None:
                # 如果prev没有设置，用另一种方式
                # he.next.next 应该回到 he，所以 he.next.next.vertex 是起点
                v_start = he.next.next.vertex
            
            edge_map[(id(v_start), id(v_end))] = he
        
        # 建立twin关系
        for he in self.halfedges:
            v_end = he.vertex
            v_start = he.next.next.vertex
            reverse_key = (id(v_end), id(v_start))
            if reverse_key in edge_map:
                twin_he = edge_map[reverse_key]
                he.twin = twin_he
                twin_he.twin = he
    
    def get_vertex_positions(self):
        """获取所有顶点位置"""
        return np.array([v.position for v in self.vertices])
    
    def get_faces_indices(self):
        """获取所有面的顶点索引"""
        faces_indices = []
        vertex_to_idx = {id(v): i for i, v in enumerate(self.vertices)}
        
        for face in self.faces:
            he = face.halfedge
            indices = []
            # 收集三个顶点
            for _ in range(3):
                indices.append(vertex_to_idx[id(he.vertex)])
                he = he.next
            # 确保是有效的三角形
            if len(set(indices)) == 3:
                faces_indices.append(indices)
        
        return faces_indices
    
    def get_vertex_one_ring_neighbors(self, vertex):
        """
        获取顶点的一环邻居（针对三角网格）
        
        注意：vertex.halfedge 是指向 vertex 的半边
        所以要找从 vertex 出发的半边，需要用 he.next
        
        策略：
        1. 从 vertex.halfedge.next 开始（这是从vertex出发的半边）
        2. 沿着 he.next.twin 循环（逆时针绕vertex）
        3. 每次收集 he.vertex（出边的终点）
        """
        neighbors = []
        if vertex.halfedge is None:
            return neighbors
        
        # vertex.halfedge 指向 vertex
        # vertex.halfedge.next 从 vertex 出发
        start_he = vertex.halfedge.next
        current_he = start_he
        
        # 逆时针遍历
        while True:
            # 收集当前出边的终点
            neighbors.append(current_he.vertex)
            
            # 移动到下一条从vertex出发的边：current_he.next.twin.next
            # 或者简化为：current_he.twin.next (如果twin存在)
            if current_he.twin is None:
                # 遇到边界
                break
            
            next_he = current_he.twin.next
            
            if next_he == start_he:
                # 回到起点，完成闭环
                return neighbors
            
            current_he = next_he
        
        # 遇到边界，反向遍历
        # 从 vertex.halfedge.prev.twin 开始（如果存在）
        current_he = vertex.halfedge
        while current_he.prev.twin is not None:
            current_he = current_he.prev.twin
            neighbors.insert(0, current_he.next.vertex)
        
        return neighbors
    
    def create_triangle(self, v0, v1, v2):
        """
        创建一个三角形面
        
        Args:
            v0, v1, v2: 三个顶点（逆时针顺序）
            
        三条半边：
        - he0: v0 -> v1
        - he1: v1 -> v2  
        - he2: v2 -> v0
        """
        face = Face()
        self.faces.append(face)
        
        # 创建三条半边
        he0 = HalfEdge()
        he1 = HalfEdge()
        he2 = HalfEdge()
        self.halfedges.extend([he0, he1, he2])
        
        # 设置半边指向的顶点（终点）
        he0.vertex = v1  # he0: v0 -> v1
        he1.vertex = v2  # he1: v1 -> v2
        he2.vertex = v0  # he2: v2 -> v0
        
        # 设置面
        he0.face = face
        he1.face = face
        he2.face = face
        
        # 设置next和prev
        he0.next = he1
        he1.next = he2
        he2.next = he0
        
        he0.prev = he2
        he1.prev = he0
        he2.prev = he1
        
        # 更新顶点的halfedge引用
        v0.halfedge = he2
        v1.halfedge = he0
        v2.halfedge = he1
        
        face.halfedge = he0
        
def load_obj(filename):
    """加载OBJ文件"""
    vertices = []
    faces = []
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                parts = line.strip().split()
                face = [int(p.split('/')[0]) - 1 for p in parts[1:4]]
                faces.append(face)
    
    return vertices, faces


def save_obj(filename, vertices, faces):
    """保存OBJ文件"""
    with open(filename, 'w') as f:
        for v in vertices:
            f.write(f'v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
        for face in faces:
            f.write(f'f {face[0]+1} {face[1]+1} {face[2]+1}\n')