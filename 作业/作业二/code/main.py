
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from framework.renderer import Renderer


class Application:
    def __init__(self):
        self.renderer = None
        self.width = 1280
        self.height = 720
        self.current_task = 1
        
    def initialize(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(b"Computer Graphics Homework 2")
        
        print("=" * 70)
        print("计算机图形学作业2")
        print("=" * 70)
        print("\n操作说明:")
        print("  数字键 1-5: 切换任务")
        print("  F: Flat Shading")
        print("  G: Gouraud Shading")
        print("  P: Phong Shading")
        print("  B: 开关Bump Mapping")
        print("  S: 开关阴影")
        print("  +/-: 拉近/拉远相机（观察纹理走样）")
        print("  H: 显示帮助")
        print("  Q/ESC: 退出")
        print("=" * 70 + "\n")
        
        self.renderer = Renderer(self.width, self.height)
        
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special_keyboard)  # 添加特殊键处理
        glutTimerFunc(16, self.timer, 0)
        
    def display(self):
        self.renderer.render()
        glutSwapBuffers()
        
    def reshape(self, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        self.renderer.camera.set_aspect(width / height)
        
    def special_keyboard(self, key, x, y):
        """处理特殊键（方向键等）"""
        if key == GLUT_KEY_UP or key == ord('+'):
            # 拉近相机
            self.renderer.camera.position.z -= 0.5
            if self.renderer.camera.position.z < 2.0:
                self.renderer.camera.position.z = 2.0
            print(f"相机距离: {self.renderer.camera.position.z:.1f}")
        elif key == GLUT_KEY_DOWN or key == ord('-'):
            # 拉远相机
            self.renderer.camera.position.z += 0.5
            if self.renderer.camera.position.z > 15.0:
                self.renderer.camera.position.z = 15.0
            print(f"相机距离: {self.renderer.camera.position.z:.1f}")
    
        glutPostRedisplay()
    
    def keyboard(self, key, x, y):
        if key in [b'q', b'Q', b'\x1b']:
            sys.exit(0)
        elif key == b'1':
            self.renderer.set_task(1)
        elif key == b'2':
            self.renderer.set_task(2)
        elif key == b'3':
            self.renderer.set_task(3)
        elif key == b'4':
            self.renderer.set_task(4)
        elif key == b'5':
            self.renderer.set_task(5)
        elif key in [b'f', b'F']:
            self.renderer.set_shading_mode('flat')
        elif key in [b'g', b'G']:
            self.renderer.set_shading_mode('gouraud')
        elif key in [b'p', b'P']:
            self.renderer.set_shading_mode('phong')
        elif key in [b'b', b'B']:
            self.renderer.toggle_bump()
        elif key in [b's', b'S']:
            self.renderer.toggle_shadow()
        elif key == b'+' or key == b'=':
            # 拉近相机
            self.renderer.camera.position.z -= 0.5
            if self.renderer.camera.position.z < 2.0:
                self.renderer.camera.position.z = 2.0
            print(f"相机距离: {self.renderer.camera.position.z:.1f}")
        elif key == b'-' or key == b'_':
            # 拉远相机
            self.renderer.camera.position.z += 0.5
            if self.renderer.camera.position.z > 15.0:
                self.renderer.camera.position.z = 15.0
            print(f"相机距离: {self.renderer.camera.position.z:.1f}")
        elif key in [b'h', b'H']:
            self.print_help()
        
        glutPostRedisplay()
    
    def timer(self, value):
        self.renderer.update(0.016)
        glutPostRedisplay()
        glutTimerFunc(16, self.timer, 0)
    
    def print_help(self):
        print("\n" + "=" * 70)
        print("帮助信息")
        print("=" * 70)
        print("当前任务:", self.renderer.current_task)
        print("=" * 70 + "\n")
    
    def run(self):
        self.initialize()
        glutMainLoop()


if __name__ == '__main__':
    app = Application()
    app.run()
