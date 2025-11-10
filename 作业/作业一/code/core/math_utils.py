"""
数学工具模块
包含矩阵变换、四元数等数学功能
"""

import numpy as np

def LookAt(eye, center, up):
    """构建视图矩阵
    参数:
        eye: 相机位置
        center: 相机看向的位置
        up: 相机上方向
    返回:
        4x4视图矩阵
    """
    
    return np.eye(4)

def Ortho(left, right, bottom, top, near, far):
    """构建正交投影矩阵
    参数：
        left (float): 左边界，视锥体左侧平面的x坐标
        right (float): 右边界，视锥体右侧平面的x坐标
        bottom (float): 下边界，视锥体底部平面的y坐标
        top (float): 上边界，视锥体顶部平面的y坐标
        near (float): 近平面，视锥体近端平面到相机的距离 （正值）
        far (float): 远平面，视锥体远端平面到相机的距离   (正值， near < far)
    返回：
        4x4正交投影矩阵
    """

    
    return np.eye(4)

def Perspective(fov, aspect=1.0, near=0.1, far=10.0):
    """构建透视投影矩阵
    参数：
        fov (float): 垂直视野角度（Field of View Y），单位为度（degrees）
        aspect (float): 宽高比（aspect ratio），默认值为1.0
        near (float): 近平面，视锥体近端平面到相机的距离 （正值）
        far (float): 远平面，视锥体远端平面到相机的距离   (正值， near < far)
    返回：
        4x4透视投影矩阵
    """
    
    return np.eye(4)

class Quaternion:
    """四元数类，用于表示旋转"""
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w = w  # 实部
        self.x = x  # 虚部i
        self.y = y  # 虚部j
        self.z = z  # 虚部k
    
    @classmethod
    def from_axis_angle(cls, axis, angle):
        """从轴角表示创建四元数"""
        axis = axis / np.linalg.norm(axis)
        half_angle = angle / 2
        sin_half = np.sin(half_angle)
        cos_half = np.cos(half_angle)
        
        return cls(cos_half, axis[0] * sin_half, axis[1] * sin_half, axis[2] * sin_half)
    
    @classmethod
    def from_euler(cls, rx, ry, rz):
        """从欧拉角创建四元数（ZYX顺序）"""
        qx = cls.from_axis_angle(np.array([1, 0, 0]), rx)
        qy = cls.from_axis_angle(np.array([0, 1, 0]), ry)
        qz = cls.from_axis_angle(np.array([0, 0, 1]), rz)
        
        return qz * qy * qx
    
    def normalize(self):
        """归一化四元数"""
        norm = np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        if norm > 1e-8:
            self.w /= norm
            self.x /= norm
            self.y /= norm
            self.z /= norm
        return self
    
    def conjugate(self):
        """四元数共轭"""
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    def __mul__(self, other):
        """四元数乘法"""
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        else:
            return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)
    
    def __add__(self, other):
        """四元数加法"""
        return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)
    
    def dot(self, other):
        """四元数点积"""
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z
    
    def to_rotation_matrix(self):
        """转换为3x3旋转矩阵"""
        self.normalize()
        
        return np.eye(3)
    
    @staticmethod
    def slerp(q1, q2, t):
        """球面线性插值"""
        q1.normalize()
        q2.normalize()
        
        
        return q1
