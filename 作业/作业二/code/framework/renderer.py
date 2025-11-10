import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders as gl_shaders
import glm
import os

from framework.geometry import create_sphere, create_plane
from framework.texture_loader import load_texture
from framework.camera import Camera


class Renderer:
    def __init__(self, width, height):
        self.camera = Camera()
        self.current_task = 1
        self.shading_mode = 'gouraud'
        self.bump_strength = 300.0
        self.use_bump = False
        self.use_shadow = False
        self.time = 0.0
        
        self.shaders = {}
        self.textures = {}
        self.sphere_vao = None
        self.sphere_count = 0
        self.plane_vao = None
        self.plane_count = 0
        
        self.shadow_fbo = None
        self.shadow_map = None
        self.shadow_width = 2048
        self.shadow_height = 2048
        
        self.window_width = width
        self.window_height = height
        self._initialize()
    
    def _initialize(self):
        """初始化渲染器"""
        print("初始化渲染器...")
        
        self._load_shaders()
        self._load_textures()
        self._create_geometry()
        self._create_shadow_map()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        
        print("✓ 渲染器初始化完成\n")
    
    def _load_shaders(self):
        """加载所有着色器"""
        print("  加载着色器...")
        
        shader_configs = [
            ('task1', 'task1_sphere.vert', 'task1_sphere.frag'),
            ('task2', 'task1_sphere.vert', 'task2_antialias.frag'),
            ('task3_flat', 'task3_flat.vert', 'task3_flat.frag'),
            ('task3_gouraud', 'task3_gouraud.vert', 'task3_gouraud.frag'),
            ('task3_phong', 'task3_phong.vert', 'task3_phong.frag'),
            ('task4', 'task3_phong.vert', 'task4_bump.frag'),
            ('task5', 'task5_shadow.vert', 'task5_shadow.frag'),
            ('shadow_depth', 'shadow_depth.vert', 'shadow_depth.frag'),
        ]
        
        for name, vert_file, frag_file in shader_configs:
            try:
                vert_src = self._load_shader_file(f'shaders/{vert_file}')
                frag_src = self._load_shader_file(f'shaders/{frag_file}')
                
                program = gl_shaders.compileProgram(
                    gl_shaders.compileShader(vert_src, GL_VERTEX_SHADER),
                    gl_shaders.compileShader(frag_src, GL_FRAGMENT_SHADER)
                )
                
                link_status = glGetProgramiv(program, GL_LINK_STATUS)
                if not link_status:
                    info_log = glGetProgramInfoLog(program)
                    print(f"    ✗ {name} 链接失败: {info_log.decode()}")
                    continue
                
                self.shaders[name] = program
                print(f"    ✓ {name}")
            except Exception as e:
                print(f"    ✗ {name}: {e}")
    
    def _load_shader_file(self, path):
        """读取着色器文件"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    #def _load_textures(self):
    #    """加载纹理"""
    #    print("  加载纹理...")
    #    
    #    texture_files = {
    #        'earth': 'resources/earthmap.jpg',
    #        'bump': 'resources/earthbump.jpg',
    #        'plane': 'resources/chessboard.jpg',
    #    }
    #    
    #    for name, path in texture_files.items():
    #        self.textures[name] = load_texture(path)
    #        print(f"    ✓ {name}")
            
            
    def _load_textures(self):
        """加载纹理"""
        print("  加载纹理...")
    
        # 为 Task1 加载无过滤的纹理（会产生锯齿）
        try:
            from framework.texture_loader import load_texture_no_filter, load_texture_with_mipmap
            self.textures['earth_no_filter'] = load_texture_no_filter('resources/earthmap.jpg')
            print(f"    ✓ earth_no_filter (无过滤)")
        except Exception as e:
            print(f"    ✗ earth_no_filter: {e}")
    
        # 为 Task2 加载带 mipmap 的纹理（平滑）
        try:
            self.textures['earth'] = load_texture_with_mipmap('resources/earthmap.jpg')
            print(f"    ✓ earth (带 mipmap)")
        except Exception as e:
            print(f"    ✗ earth: {e}")
    
        # Bump map
        try:
            self.textures['bump'] = load_texture('resources/earthbump.jpg')
            print(f"    ✓ bump")
        except Exception as e:
            print(f"    ✗ bump: {e}")
    
        # 平面纹理
        try:
            self.textures['plane'] = load_texture('resources/chessboard.jpg')
            print(f"    ✓ plane")
        except Exception as e:
            print(f"    ✗ plane: {e}")

    
    def _create_geometry(self):
        """创建几何体"""
        print("  创建几何体...")
        
        # 球体
        positions, texcoords, normals = create_sphere()
        self.sphere_count = len(positions)
        self.sphere_vao = self._create_vao(positions, texcoords, normals)
        print(f"    ✓ 球体: {self.sphere_count} 顶点")
        
        # 平面
        positions, texcoords, normals = create_plane()
        self.plane_count = len(positions)
        self.plane_vao = self._create_vao(positions, texcoords, normals)
        print(f"    ✓ 平面: {self.plane_count} 顶点")
    
    def _create_vao(self, positions, texcoords, normals):
        """创建VAO"""
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        
        total_size = positions.nbytes + texcoords.nbytes + normals.nbytes
        glBufferData(GL_ARRAY_BUFFER, total_size, None, GL_STATIC_DRAW)
        
        offset = 0
        glBufferSubData(GL_ARRAY_BUFFER, offset, positions.nbytes, positions)
        offset += positions.nbytes
        glBufferSubData(GL_ARRAY_BUFFER, offset, texcoords.nbytes, texcoords)
        offset += texcoords.nbytes
        glBufferSubData(GL_ARRAY_BUFFER, offset, normals.nbytes, normals)
        
        # 位置
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # 纹理坐标
        offset = positions.nbytes
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)
        
        # 法线
        offset += texcoords.nbytes
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(2)
        
        glBindVertexArray(0)
        return vao
    
    def _create_shadow_map(self):
        """创建阴影贴图"""
        print("  创建阴影贴图...")
        
        # 创建帧缓冲对象
        self.shadow_fbo = glGenFramebuffers(1)
        
        # 创建深度纹理
        self.shadow_map = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.shadow_map)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, 
                     self.shadow_width, self.shadow_height, 0, 
                     GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        border_color = [1.0, 1.0, 1.0, 1.0]
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)
        
        # 绑定深度纹理到帧缓冲
        glBindFramebuffer(GL_FRAMEBUFFER, self.shadow_fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, 
                              GL_TEXTURE_2D, self.shadow_map, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        
        # 检查帧缓冲完整性
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("    ✗ 阴影帧缓冲不完整")
        else:
            print("    ✓ 阴影贴图")
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def _get_light_space_matrix(self):
        """获取光源空间矩阵"""
        light_pos = glm.vec3(4.0, 4.0, 4.0)
        light_projection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 20.0)
        light_view = glm.lookAt(light_pos, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
        return light_projection * light_view
    
    def _render_shadow_map(self):
        """渲染阴影贴图"""
        if 'shadow_depth' not in self.shaders:
            return
        
        light_space_matrix = self._get_light_space_matrix()
        
        glViewport(0, 0, self.shadow_width, self.shadow_height)
        glBindFramebuffer(GL_FRAMEBUFFER, self.shadow_fbo)
        glClear(GL_DEPTH_BUFFER_BIT)
        
        shader = self.shaders['shadow_depth']
        glUseProgram(shader)
        
        # 渲染球体
        model = self._get_sphere_model()
        mvp = light_space_matrix * model
        glUniformMatrix4fv(glGetUniformLocation(shader, "lightSpaceMatrix"), 
                          1, GL_FALSE, glm.value_ptr(mvp))
        
        glBindVertexArray(self.sphere_vao)
        glDrawArrays(GL_TRIANGLES, 0, self.sphere_count)
        
        # 渲染平面
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, -1.5, 0.0))
        mvp = light_space_matrix * model
        glUniformMatrix4fv(glGetUniformLocation(shader, "lightSpaceMatrix"), 
                          1, GL_FALSE, glm.value_ptr(mvp))
        
        glBindVertexArray(self.plane_vao)
        glDrawArrays(GL_TRIANGLES, 0, self.plane_count)
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glUseProgram(0)
        
    def render(self):
        """主渲染函数"""
        # 如果是任务5，先渲染阴影贴图
        if self.current_task == 5 or self.use_shadow:
            self._render_shadow_map()
        
        # 恢复视口
        glViewport(0, 0, self.window_width, self.window_height)  # 这里应该使用实际窗口大小
        
        glClearColor(0.1, 0.1, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 根据当前任务选择着色器
        if self.current_task == 1:
            shader = self.shaders.get('task1')
        elif self.current_task == 2:
            shader = self.shaders.get('task2')
        elif self.current_task == 3:
            shader = self.shaders.get(f'task3_{self.shading_mode}')
        elif self.current_task == 4:
            shader = self.shaders.get('task4')
        elif self.current_task == 5:
            shader = self.shaders.get('task5')
        else:
            shader = self.shaders.get('task1')
        
        if shader is None:
            print(f"警告: 着色器未加载")
            return
        
        glUseProgram(shader)
        
        # 设置矩阵
        view = self.camera.get_view_matrix()
        proj = self.camera.get_projection_matrix()
        model = self._get_sphere_model()
        mvp = proj * view * model
        
        glUniformMatrix4fv(glGetUniformLocation(shader, "MVP"), 1, GL_FALSE, glm.value_ptr(mvp))
        glUniformMatrix4fv(glGetUniformLocation(shader, "M"), 1, GL_FALSE, glm.value_ptr(model))
        
        normal_matrix = glm.transpose(glm.inverse(glm.mat3(model)))
        glUniformMatrix3fv(glGetUniformLocation(shader, "normalMatrix"), 1, GL_FALSE, glm.value_ptr(normal_matrix))
        
        # 设置光照参数
        light_pos = [5.0, 3.0, 5.0]
        glUniform3f(glGetUniformLocation(shader, "lightPos"), *light_pos)
        glUniform3f(glGetUniformLocation(shader, "viewPos"), 
                   self.camera.position.x, self.camera.position.y, self.camera.position.z)
        glUniform3f(glGetUniformLocation(shader, "lightColor"), 1.0, 1.0, 1.0)
        glUniform1f(glGetUniformLocation(shader, "lightIntensity"), 50.0)
        
        # 任务5需要光源空间矩阵
        if self.current_task == 5 or self.use_shadow:
            light_space_matrix = self._get_light_space_matrix()
            glUniformMatrix4fv(glGetUniformLocation(shader, "lightSpaceMatrix"), 
                              1, GL_FALSE, glm.value_ptr(light_space_matrix))
        
        # 绑定纹理
        glActiveTexture(GL_TEXTURE0)
        
        if self.current_task == 1:
            # Task1: 使用无过滤纹理，会产生明显锯齿
            glBindTexture(GL_TEXTURE_2D, self.textures.get('earth_no_filter', self.textures['earth']))
        else:
            # Task2 及以后: 使用带 mipmap 的平滑纹理
            glBindTexture(GL_TEXTURE_2D, self.textures['earth'])
        
        glUniform1i(glGetUniformLocation(shader, "texDiffuse"), 0)
        
        if self.current_task == 4 or self.use_bump:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.textures['bump'])
            glUniform1i(glGetUniformLocation(shader, "texBump"), 1)
            glUniform1f(glGetUniformLocation(shader, "bumpStrength"), self.bump_strength)
        
        if self.current_task == 5 or self.use_shadow:
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D, self.shadow_map)
            glUniform1i(glGetUniformLocation(shader, "shadowMap"), 2)
        
        # 渲染球体
        glBindVertexArray(self.sphere_vao)
        glDrawArrays(GL_TRIANGLES, 0, self.sphere_count)
        
        # 任务5渲染平面
        if self.current_task == 5:
            model = glm.mat4(1.0)
            model = glm.translate(model, glm.vec3(0.0, -1.5, 0.0))
            mvp = proj * view * model
            glUniformMatrix4fv(glGetUniformLocation(shader, "MVP"), 1, GL_FALSE, glm.value_ptr(mvp))
            glUniformMatrix4fv(glGetUniformLocation(shader, "M"), 1, GL_FALSE, glm.value_ptr(model))
            
            if self.use_shadow:
                light_space_matrix = self._get_light_space_matrix()
                glUniformMatrix4fv(glGetUniformLocation(shader, "lightSpaceMatrix"), 
                                  1, GL_FALSE, glm.value_ptr(light_space_matrix))
            
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.textures['plane'])
            
            glBindVertexArray(self.plane_vao)
            glDrawArrays(GL_TRIANGLES, 0, self.plane_count)
        
        glUseProgram(0)
    
    def _get_sphere_model(self):
        """获取球体模型矩阵"""
        model = glm.mat4(1.0)
        model = glm.rotate(model, glm.radians(self.time * 10), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(23.5), glm.vec3(0, 0, 1))
        return model
    
    def update(self, delta_time):
        """更新"""
        self.time += delta_time
    
    def set_task(self, task):
        """设置任务"""
        self.current_task = task
        print(f"\n>>> 切换到任务 {task}")
    
    def set_shading_mode(self, mode):
        """设置光照模式"""
        self.shading_mode = mode
        print(f"\n>>> 光照模式: {mode}")
    
    def toggle_bump(self):
        """切换Bump Mapping"""
        self.use_bump = not self.use_bump
        print(f"\n>>> Bump Mapping: {'开启' if self.use_bump else '关闭'}")
    
    def toggle_shadow(self):
        """切换阴影"""
        self.use_shadow = not self.use_shadow
        print(f"\n>>> 阴影: {'开启' if self.use_shadow else '关闭'}")
