import math

from pyglm import glm


class Camera:
    def __init__(self):
        self.position = glm.vec3(0.0, 0.0, 4.0)
        self.target = self.position + glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.fov = 60.0
        self.aspect = 16.0 / 9.0
        self.near = 0.1
        self.far = 10000.0

        # 是否正在移动
        self.moving_forward = False
        self.moving_backward = False
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.target, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.fov), self.aspect, self.near, self.far)

    def set_aspect(self, aspect):
        self.aspect = aspect

    # 新增：相机移动
    def tick(self):
        if self.moving_forward:
            self.move_forward()
        if self.moving_backward:
            self.move_backward()
        if self.moving_left:
            self.move_left()
        if self.moving_right:
            self.move_right()
        if self.moving_up:
            self.move_up()
        if self.moving_down:
            self.move_down()

    def move_forward(self, distance=0.1):
        phi = self._get_phi()
        delta = glm.vec3(math.cos(phi), 0.0, math.sin(phi)) * distance
        self.position += delta
        self.target += delta

    def move_backward(self, distance=0.1):
        self.move_forward(-distance)

    def move_left(self, distance=0.1):
        phi = self._get_phi()
        delta = glm.vec3(math.sin(phi), 0.0, -math.cos(phi)) * distance
        self.position += delta
        self.target += delta

    def move_right(self, distance=0.1):
        self.move_left(-distance)

    def move_up(self, distance=0.1):
        self.position.y += distance
        self.target.y += distance

    def move_down(self, distance=0.1):
        self.move_up(-distance)

    def _get_phi(self):
        """
        返回相机的方位角，弧度
        x 轴正方向是 0，z 轴正方向是 π/2，x 轴负方向是 ±π，z 轴负方向是 -π/2
        """
        sight = self.target - self.position
        return math.atan2(sight.z, sight.x)

    def _get_theta(self):
        """
        返回相机的俯仰角，弧度
        水平是 0，向下是 -π/2，向上是 π/2
        """
        sight = self.target - self.position
        return math.atan2(sight.y, math.sqrt(sight.x**2 + sight.z**2))

    # 新增：调整相机视角
    def angle_change(self, delta_theta=0, delta_phi=0):
        # 旧的经纬值
        phi, theta = self._get_phi(), self._get_theta()

        # 更新经纬值
        phi = phi + delta_theta
        if phi > math.pi:
            phi -= math.tau
        elif phi < -math.pi:
            phi += math.tau
        theta = max(-math.pi / 2 + 0.0001, min(math.pi / 2 - 0.0001, theta + delta_phi))

        # 根据经纬算出视线方向的单位向量
        xz, y = math.cos(theta), math.sin(theta)
        x, z = xz * math.cos(phi), xz * math.sin(phi)

        self.target = self.position + glm.vec3(x, y, z)

    def reset(self):
        self.position = glm.vec3(0.0, 0.0, 4.0)
        self.target = self.position + glm.vec3(0.0, 0.0, -1.0)
