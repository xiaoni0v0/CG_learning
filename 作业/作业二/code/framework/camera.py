import glm


class Camera:
    def __init__(self):
        self.position = glm.vec3(0.0, 0.0, 4.0)
        self.target = glm.vec3(0.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.fov = 60.0
        self.aspect = 16.0 / 9.0
        self.near = 0.1
        self.far = 100.0
    
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.target, self.up)
    
    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.fov), self.aspect, self.near, self.far)
    
    def set_aspect(self, aspect):
        self.aspect = aspect
