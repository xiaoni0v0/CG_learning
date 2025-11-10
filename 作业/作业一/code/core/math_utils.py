"""
数学工具模块
包含矩阵变换、四元数等数学功能
"""

from typing import Self

import numpy as np


def LookAt(eye: np.ndarray, center: np.ndarray, up: np.ndarray) -> np.ndarray:
    """
    构建视图矩阵
    参数:
        eye: 相机位置
        center: 相机看向的位置
        up: 相机上方向
    返回:
        4x4视图矩阵
    """

    z = (eye - center) / np.linalg.norm(eye - center)
    x = np.cross(up, z) / np.linalg.norm(np.cross(up, z))
    y = np.cross(z, x)

    return np.array(
        [
            [x[0], x[1], x[2], -np.dot(eye, x)],
            [y[0], y[1], y[2], -np.dot(eye, y)],
            [z[0], z[1], z[2], -np.dot(eye, z)],
            [0, 0, 0, 1],
        ]
    )


def Ortho(
    left: float, right: float, bottom: float, top: float, near: float, far: float
) -> np.ndarray:
    """
    构建正交投影矩阵
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

    return np.array(
        [
            [2 / (right - left), 0, 0, -(right + left) / (right - left)],
            [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
            [0, 0, -2 / (far - near), -(far + near) / (far - near)],
            [0, 0, 0, 1],
        ]
    )


def Perspective(
    fov: float, aspect: float = 1.0, near: float = 0.1, far: float = 10.0
) -> np.ndarray:
    """
    构建透视投影矩阵
    参数：
        fov (float): 垂直视野角度（Field of View Y），单位为度（degrees）
        aspect (float): 宽高比（aspect ratio），默认值为1.0
        near (float): 近平面，视锥体近端平面到相机的距离 （正值）
        far (float): 远平面，视锥体远端平面到相机的距离   (正值， near < far)
    返回：
        4x4透视投影矩阵
    """

    cot_half_fov = 1 / np.tan(np.radians(fov / 2))

    return np.array(
        [
            [cot_half_fov / aspect, 0, 0, 0],
            [0, cot_half_fov, 0, 0],
            [0, 0, -(far + near) / (far - near), -2 * far * near / (far - near)],
            [0, 0, -1, 0],
        ]
    )


class Quaternion:
    """四元数类，用于表示旋转"""

    def __init__(self, w: float = 1.0, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.w = w  # 实部
        self.x = x  # 虚部 i
        self.y = y  # 虚部 j
        self.z = z  # 虚部 k

    @classmethod
    def from_axis_angle(cls, axis: np.ndarray, angle: float) -> "Quaternion":
        """从轴角表示创建四元数"""
        axis = axis / np.linalg.norm(axis)
        half_angle = angle / 2
        sin_half = np.sin(half_angle)
        cos_half = np.cos(half_angle)

        return cls(cos_half, axis[0] * sin_half, axis[1] * sin_half, axis[2] * sin_half)

    @classmethod
    def from_euler(cls, rx: float, ry: float, rz: float) -> "Quaternion":
        """从欧拉角创建四元数（ZYX顺序）"""
        qx = cls.from_axis_angle(np.array([1, 0, 0]), rx)
        qy = cls.from_axis_angle(np.array([0, 1, 0]), ry)
        qz = cls.from_axis_angle(np.array([0, 0, 1]), rz)

        return qz * qy * qx

    def normalize(self) -> "Quaternion":
        """归一化四元数"""
        norm = np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        if norm > 1e-8:
            self.w /= norm
            self.x /= norm
            self.y /= norm
            self.z /= norm
        return self

    def conjugate(self) -> "Quaternion":
        """四元数共轭"""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def __add__(self, other: "Quaternion") -> "Quaternion":
        """四元数加法"""
        assert isinstance(other, Quaternion)
        return Quaternion(
            self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z
        )

    def __mul__(self, other: int | float | Self) -> "Quaternion":
        """四元数乘法"""
        assert isinstance(other, (int, float, Quaternion))
        if isinstance(other, Quaternion):
            w = (
                self.w * other.w
                - self.x * other.x
                - self.y * other.y
                - self.z * other.z
            )
            x = (
                self.w * other.x
                + self.x * other.w
                + self.y * other.z
                - self.z * other.y
            )
            y = (
                self.w * other.y
                - self.x * other.z
                + self.y * other.w
                + self.z * other.x
            )
            z = (
                self.w * other.z
                + self.x * other.y
                - self.y * other.x
                + self.z * other.w
            )
            return Quaternion(w, x, y, z)
        else:
            return Quaternion(
                self.w * other, self.x * other, self.y * other, self.z * other
            )

    def dot(self, other: "Quaternion") -> float:
        """四元数点积"""
        assert isinstance(other, Quaternion)
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z

    def to_rotation_matrix(self) -> np.ndarray:
        """转换为3x3旋转矩阵"""
        self.normalize()

        a, b, c, d = self.w, self.x, self.y, self.z
        return np.array(
            [
                [a**2 + b**2 - c**2 - d**2, 2 * (b * c - a * d), 2 * (b * d + a * c)],
                [2 * (b * c + a * d), a**2 - b**2 + c**2 - d**2, 2 * (c * d - a * b)],
                [2 * (b * d - a * c), 2 * (c * d + a * b), a**2 - b**2 - c**2 + d**2],
            ]
        )

    @staticmethod
    def slerp(q1: "Quaternion", q2: "Quaternion", t: float) -> "Quaternion":
        """球面线性插值"""
        q1.normalize()
        q2.normalize()

        dot = q1.dot(q2)

        alpha = np.acos(max(-1.0, min(dot, 1.0)))
        sin_alpha = np.sin(alpha)
        sin_t_alpha = np.sin(t * alpha)
        sin_1t_alpha = np.sin((1 - t) * alpha)

        return (q1 * sin_1t_alpha + q2 * sin_t_alpha) * (1.0 / sin_alpha)
