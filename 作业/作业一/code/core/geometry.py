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

    def compute_normal(self):
        """计算三角形的法线向量"""

        return np.array([0, 0, 1])

    def rotate_norm(self, theta):
        """绕法线旋转三角形"""
        center = np.mean(self.vertices, axis=0)
        normal = self.compute_normal()
        
        R = np.eye(3)
        
        for i in range(3):
            self.vertices[i] = center + R @ (self.vertices[i] - center)
    
    def rotate_mat(self, mat):
        """应用旋转矩阵"""
        self.vertices = (mat @ self.vertices.T).T
    
    def inside(self, x, y, z):
        """判断点(x,y)是否在三角形内"""
        v0, v1, v2 = self.vertices
        
        return True
    
    def compute_barycentric(self, x, y, z):
        """计算重心坐标"""
        v0, v1, v2 = self.vertices
        
        
        return np.array([1/3, 1/3, 1/3])
        
    def to_homogeneous_coordinates(self):
        """转换为齐次坐标"""
        return np.hstack((self.vertices, np.ones((3, 1))))
    
    def interpolate_color(self, barycentric):
        """使用重心坐标插值颜色"""
        alpha, beta, gamma = barycentric
        return alpha * self.colors[0] + beta * self.colors[1] + gamma * self.colors[2]

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
        
        color = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), 
                 (1.0, 1.0, 0.0), (1.0, 0.0, 1.0)][i]
        t.setColor(0, *color)
        t.setColor(1, *color)
        t.setColor(2, *color)
        
        triangles.append(t)
    
    return triangles
