"""
光栅化器模块
包含光栅化算法和渲染功能
"""

import numpy as np
from PIL import Image
from .geometry import Triangle

class Rasterization:
    """光栅化器类"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color_buf = np.zeros((height, width, 3))
        self.depth_buf = np.ones((height, width)) * np.finfo(np.float32).max
        self.view_m = np.eye(4)
        self.proj_m = np.eye(4)
        self.enable_antialiasing = False
        self.enable_depth_test = False
        self.sample_points = [(0.0, 0.0)]

    def clear_buffers(self):
        """清除缓冲区"""
        self.color_buf = np.zeros((self.height, self.width, 3))
        self.depth_buf = np.ones((self.height, self.width)) * np.finfo(np.float32).max

    def setViewM(self, mat):
        self.view_m = mat

    def setProjM(self, mat):
        self.proj_m = mat
    
    def enableAntialiasing(self, enable=True, samples=2):
        """
        启用/禁用抗锯齿
        
        Args:
            enable: 是否启用抗锯齿
            samples: 采样密度，samples x samples 个采样点
        """
        self.enable_antialiasing = enable
        msaa_samples = max(1, samples)  # 至少1x1

        self.sample_points = self._generate_sample_points(msaa_samples)

    
    def enableDepthTest(self, enable=True):
        """启用/禁用深度测试"""
        self.enable_depth_test = enable
    
    def _generate_sample_points(self, samples):
        """
        生成MSAA采样点
        
        Args:
            samples: 采样密度 (samples x samples)
            
        Returns:
            采样点列表 [(dx, dy), ...]
        """
        if samples == 1:
            return [(0.0, 0.0)]  # 中心采样
        
        # 生成均匀分布的采样点
        step = 1.0 / samples
        offset = step * 0.5 - 0.5  # 居中偏移
        
        sample_points = []
        for i in range(samples):
            for j in range(samples):
                dx = offset + i * step
                dy = offset + j * step
                sample_points.append((dx, dy))
        
        return sample_points
    
    def rasterize_triangle(self, t):
        """光栅化一个三角形"""
        H, W, _ = self.color_buf.shape

        # 变换到裁剪空间
        v4 = t.to_homogeneous_coordinates()
        v4 = (self.proj_m @ self.view_m @ v4.T).T
        
        # 保存深度值
        depth_values = v4[:, 2].copy() / v4[:, 3].copy()
        
        # 透视除法
        v4[:, :3] = v4[:, :3] / v4[:, 3:4]
        
        # 变换到NDC空间
        v4[:, :3] = v4[:, :3] * 0.5 + 0.5
        
        # 变换到屏幕空间
        screen_t = Triangle()
        for i in range(3):
            screen_x = v4[i, 0] * W
            screen_y = (1.0 - v4[i, 1]) * H  # 翻转Y轴：1-y
            screen_t.setVertex(i, screen_x, screen_y, depth_values[i])
            screen_t.setColor(i, t.colors[i, 0], t.colors[i, 1], t.colors[i, 2])
        
        # 计算边界框
        vertices = screen_t.vertices
        min_x = max(0, int(min(vertices[:, 0])))
        max_x = min(W - 1, int(max(vertices[:, 0]) + 1))
        min_y = max(0, int(min(vertices[:, 1])))
        max_y = min(H - 1, int(max(vertices[:, 1]) + 1))
        
        # 光栅化
        if self.enable_antialiasing:
            self._rasterize_msaa(screen_t, min_x, max_x, min_y, max_y)
        else:
            self._rasterize_standard(screen_t, min_x, max_x, min_y, max_y)
    
    def _rasterize_standard(self, t, min_x, max_x, min_y, max_y):
        """标准光栅化"""
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if t.inside(x + 0.5, y + 0.5, 0):
                    barycentric = t.compute_barycentric(x + 0.5, y + 0.5, 0)
                    
                    color = t.interpolate_color(barycentric)
                    self.color_buf[y, x] = color                        
    
    def _rasterize_msaa(self, t, min_x, max_x, min_y, max_y):
        """MSAA抗锯齿光栅化"""

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if t.inside(x + 0.5, y + 0.5, 0):
                    barycentric = t.compute_barycentric(x + 0.5, y + 0.5, 0)
                    
                    color = t.interpolate_color(barycentric)
                    self.color_buf[y, x] = color   
                    
    
    def render(self, t_list):
        """渲染三角形列表"""
        self.clear_buffers()
        for t in t_list:
            self.rasterize_triangle(t)
    
    def save_image(self, filename):
        """保存图像"""
        Image.fromarray((np.clip(self.color_buf, 0, 1) * 255).astype("uint8")).save(filename)
    
    def show_image(self):
        """显示图像"""
        Image.fromarray((np.clip(self.color_buf, 0, 1) * 255).astype("uint8")).show()
