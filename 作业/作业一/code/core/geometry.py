"""
几何体定义模块
包含三角形类和相关几何操作
"""

import numpy as np


class Triangle:
    """三角形类"""

    def __init__(self):
        self.vertices = np.zeros((3, 3))
        self.normals = np.zeros((3, 3))
        self.colors = np.zeros((3, 3))

    def setVertex(self, ind, x, y, z):
        self.vertices[ind] = np.array([x, y, z])

    def setColor(self, ind, r, g, b):
        self.colors[ind] = np.array([r, g, b])

    def setNormal(self, ind, nx, ny, nz):
        self.normals[ind] = np.array([nx, ny, nz])

    def compute_normal(self) -> np.ndarray:
        """计算三角形的法线向量"""

        v0, v1, v2 = self.vertices
        n = np.cross(v1 - v0, v2 - v0)
        return n / np.linalg.norm(n)

    def rotate_norm(self, theta: float) -> None:
        """绕法线旋转三角形，theta 为角度"""
        center = np.mean(self.vertices, axis=0)  # 中心坐标
        n = self.compute_normal()  # 法线向量

        I = np.eye(3)
        theta = np.radians(theta)
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        N = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])

        R = cos_theta * I + (1 - cos_theta) * np.outer(n, n) + sin_theta * N

        # 每个顶点都要应用旋转矩阵
        for i in range(3):
            self.vertices[i] = center + R @ (self.vertices[i] - center)

    def rotate_mat(self, mat):
        """应用旋转矩阵"""
        self.vertices = (mat @ self.vertices.T).T

    def inside(
        self, x: float, y: float, _: float, barycentric: np.ndarray = None
    ) -> bool:
        """
        判断点 (x, y) 是否在三角形内
        """

        a, b, c = (
            barycentric
            if barycentric is not None
            else self.compute_barycentric(x, y, _)
        )
        return a >= 0 and b >= 0 and c >= 0

        # 以下代码太慢了，不用这种形式了
        # v0, v1, v2 = self.vertices.copy()
        # v0[2], v1[2], v2[2] = 0, 0, 0  # 去掉z坐标
        # p = np.array([x, y, 0])
        #
        # n = np.cross(v1 - v0, v2 - v0)
        # a = np.cross(v0 - p, v1 - p).dot(n)
        # b = np.cross(v1 - p, v2 - p).dot(n)
        # c = np.cross(v2 - p, v0 - p).dot(n)
        #
        # return a >= 0 and b >= 0 and c >= 0

    def compute_barycentric(self, x: float, y: float, _: float) -> np.ndarray:
        """计算重心坐标"""

        def cross_z(x1: float, y1: float, x2: float, y2: float) -> float:
            """返回两个z分量为0的向量叉乘的z分量"""
            return x1 * y2 - x2 * y1

        (xA, yA, _), (xB, yB, _), (xC, yC, _) = self.vertices

        S = cross_z(xB - xA, yB - yA, xC - xA, yC - yA)
        c = cross_z(xA - x, yA - y, xB - x, yB - y) / S
        a = cross_z(xB - x, yB - y, xC - x, yC - y) / S
        b = cross_z(xC - x, yC - y, xA - x, yA - y) / S

        return np.array((a, b, c))

        # 以下代码太慢了，不用这种形式了
        # v0, v1, v2 = self.vertices.copy()
        # v0[2], v1[2], v2[2] = 0, 0, 0  # 去掉z坐标
        # p = np.array([x, y, 0])
        #
        # SC = np.linalg.norm(np.cross(v0 - p, v1 - p))
        # SA = np.linalg.norm(np.cross(v1 - p, v2 - p))
        # SB = np.linalg.norm(np.cross(v2 - p, v0 - p))
        #
        # res = np.array([SA, SB, SC])
        #
        # return res / res.sum()

    def to_homogeneous_coordinates(self):
        """转换为齐次坐标"""
        return np.hstack((self.vertices, np.ones((3, 1))))

    def interpolate_depth(self, barycentric: np.ndarray) -> np.ndarray:
        """使用重心坐标插值深度"""
        return barycentric.dot(self.vertices[:, 2])

    def interpolate_color(self, barycentric: np.ndarray) -> np.ndarray:
        """使用重心坐标插值颜色"""
        return barycentric.dot(self.colors)


# 几何体创建辅助函数
def create_jagged_triangle():
    """创建锯齿明显的三角形"""
    t = Triangle()
    t.setVertex(0, 0, 1.5, 0.0)
    t.setVertex(1, -1.5, -1.5, 0.0)
    t.setVertex(2, 1.5, -1.5, 0.0)

    t.setColor(0, 1.0, 0.0, 0.0)  # 红色
    t.setColor(1, 0.0, 1.0, 0.0)  # 绿色
    t.setColor(2, 0.0, 0.0, 1.0)  # 蓝色

    return t


def create_thin_triangles():
    """创建多个细长三角形"""
    triangles = []

    for i in range(5):
        t = Triangle()
        offset = (i - 2) * 0.5

        t.setVertex(0, offset, 2.0, 0.0)
        t.setVertex(1, offset - 0.1, -2.0, 0.0)
        t.setVertex(2, offset + 0.1, -2.0, 0.0)

        color = [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
            (1.0, 0.0, 1.0),
        ][i]
        t.setColor(0, *color)
        t.setColor(1, *color)
        t.setColor(2, *color)

        triangles.append(t)

    return triangles
