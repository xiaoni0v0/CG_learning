# bezier_circle.py
import matplotlib.pyplot as plt
import numpy as np


class BezierCurve:
    """Bezier曲线类"""

    def __init__(self, control_points):
        """
        初始化Bezier曲线

        Args:
            control_points: numpy array of shape (n, 2), n个控制点
        """
        self.control_points = np.array(control_points)
        self.degree = len(control_points) - 1

    def de_casteljau(self, t):
        """
        de Casteljau算法计算曲线上的点

        Args:
            t: 参数值，范围[0, 1]

        Returns:
            numpy array of shape (2,): 曲线上t对应的点坐标

        提示：
        1. 使用递归或迭代的方式实现de Casteljau算法
        2. 每次迭代，相邻控制点线性插值
        3. 最终得到一个点即为曲线上的点
        """

        ls = list(self.control_points)
        while len(ls) > 1:
            ls = [(1 - t) * ls[i] + t * ls[i + 1] for i in range(len(ls) - 1)]
        return ls[0]

    def evaluate(self, num_samples=100):
        """
        评估曲线上的多个点

        Args:
            num_samples: 采样点数量

        Returns:
            numpy array of shape (num_samples, 2): 曲线上的点
        """
        t_values = np.linspace(0, 1, num_samples)
        curve_points = np.array([self.de_casteljau(t) for t in t_values])
        return curve_points


class BezierCircle:
    """使用分段Bezier曲线表示圆"""

    def __init__(self, center=(0, 0), radius=1, num_segments=4):
        """
        初始化Bezier圆

        Args:
            center: 圆心坐标
            radius: 半径
            num_segments: 分段数（建议4段或8段）
        """
        self.center = np.array(center)
        self.radius = radius
        self.num_segments = num_segments
        self.segments = []
        self._create_segments()

    def _create_segments(self):
        """
        创建分段Bezier曲线来逼近圆

        提示：
        1. 将圆分成num_segments段
        2. 每段使用三次Bezier曲线（4个控制点）
        3. 对于圆，可以使用以下控制点布局：
           - P0: 段起点（在圆上）
           - P1: 起点处的切线方向控制点
           - P2: 终点处的切线方向控制点
           - P3: 段终点（在圆上）
        4. 关键参数：对于n段圆，每段圆弧对应角度为2π/n
        """

        n = self.num_segments
        pi = np.pi
        k = 4 * (1 - np.cos(pi / n)) / (3 * np.sin(pi / n))
        for i in range(n):
            # 创建Bezier曲线段
            rad = 2 * pi * i / n  # 当前圆上的点的弧度
            rad_n = 2 * pi * (i + 1) / n  # 下一个圆上的点的弧度

            p0 = self.center + self.radius * np.array([np.cos(rad), np.sin(rad)])
            p3 = self.center + self.radius * np.array([np.cos(rad_n), np.sin(rad_n)])

            p1 = p0 + k * self.radius * np.array(
                [np.cos(rad + pi / 2), np.sin(rad + pi / 2)]
            )
            p2 = p3 + k * self.radius * np.array(
                [np.cos(rad_n - pi / 2), np.sin(rad_n - pi / 2)]
            )

            control_points = np.array([p0, p1, p2, p3])
            self.segments.append(BezierCurve(control_points))

    def get_all_control_points(self):
        """获取所有控制点"""
        all_points = []
        for segment in self.segments:
            all_points.extend(segment.control_points)
        return np.array(all_points)

    def evaluate(self, num_samples_per_segment=50):
        """评估整个圆"""
        all_curve_points = []
        for segment in self.segments:
            curve_points = segment.evaluate(num_samples_per_segment)
            all_curve_points.append(curve_points)
        return np.vstack(all_curve_points)


def visualize_bezier_circle(num_segments=4):
    """可视化Bezier圆"""
    # 创建Bezier圆
    bezier_circle = BezierCircle(center=(0, 0), radius=1, num_segments=num_segments)

    # 评估曲线
    curve_points = bezier_circle.evaluate(num_samples_per_segment=50)

    # 获取控制点
    control_points = bezier_circle.get_all_control_points()

    # 绘图
    plt.figure(figsize=(10, 10))

    # 绘制曲线
    plt.plot(
        curve_points[:, 0], curve_points[:, 1], "b-", linewidth=2, label="Bezier Circle"
    )

    # 绘制控制点
    plt.plot(
        control_points[:, 0],
        control_points[:, 1],
        "ro",
        markersize=6,
        label="Control Points",
    )

    # 绘制控制多边形
    for segment in bezier_circle.segments:
        cp = segment.control_points
        plt.plot(cp[:, 0], cp[:, 1], "r--", alpha=0.5, linewidth=1)

    # 绘制真实圆（用于对比）
    theta = np.linspace(0, 2 * np.pi, 1000)
    true_circle_x = np.cos(theta)
    true_circle_y = np.sin(theta)
    plt.plot(
        true_circle_x, true_circle_y, "g--", alpha=0.5, linewidth=1, label="True Circle"
    )

    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.title(f"Bezier Circle with {num_segments} segments")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(
        f"bezier_circle_{num_segments}_segments.png", dpi=150, bbox_inches="tight"
    )
    plt.show()


if __name__ == "__main__":
    # 测试不同分段数
    for num_seg in [4, 8]:
        print(f"Creating Bezier circle with {num_seg} segments...")
        visualize_bezier_circle(num_segments=num_seg)
