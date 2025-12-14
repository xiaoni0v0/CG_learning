import math

from OpenGL.GL import *
from OpenGL.GLUT import *

from framework.renderer import Renderer


class Application:
    def __init__(self):
        self.renderer: None | Renderer = None
        self.width = 1280
        self.height = 720
        self.current_task = 1

        self.is_mouse_down = False
        self.last_mouse_pos = [0, 0]

    def initialize(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(b"Computer Graphics Homework 2")

        print("=" * 70)
        print("计算机图形学作业2")
        print("=" * 70)
        print("\n操作说明:")
        print("  数字键 1-7: 切换任务")
        print("  A S D W 空格 Shift: 上下左右前后移动")
        print("  按下鼠标拖动: 旋转相机")
        print("  R: 重置相机的位置和角度")
        print("  X: 球暂停与继续旋转")
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

        glutSetKeyRepeat(GLUT_KEY_REPEAT_OFF)  # 关闭键盘自动重复
        glutKeyboardFunc(self._keyboard_down)
        glutKeyboardUpFunc(self._keyboard_up)
        glutSpecialFunc(self._special_keyboard_down)
        glutSpecialUpFunc(self._special_keyboard_up)

        glutMouseFunc(self._mouse_button)
        glutMotionFunc(self._mouse_move)

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
        if key == GLUT_KEY_UP or key == ord("+"):
            # 拉近相机
            self.renderer.camera.position.z -= 0.5
            if self.renderer.camera.position.z < 2.0:
                self.renderer.camera.position.z = 2.0
            print(f"相机距离: {self.renderer.camera.position.z:.1f}")
        elif key == GLUT_KEY_DOWN or key == ord("-"):
            # 拉远相机
            self.renderer.camera.position.z += 0.5
            if self.renderer.camera.position.z > 15.0:
                self.renderer.camera.position.z = 15.0
            print(f"相机距离: {self.renderer.camera.position.z:.1f}")

        glutPostRedisplay()

    def _special_keyboard_down(self, key, x, y):
        # 委托给之前的 special_keyboard 函数处理
        if key in (GLUT_KEY_UP, ord("+"), GLUT_KEY_DOWN, ord("-")):
            self.special_keyboard(key, x, y)
            return

        # 实现 Shift 向下移动
        if key == 112:
            self.renderer.camera.moving_down = True

        else:
            print(f"未处理的按键: {key}")

        glutPostRedisplay()

    def _special_keyboard_up(self, key, x, y):
        if key == 112:
            self.renderer.camera.moving_down = False

        else:
            print(f"未处理的按键: {key}")

        glutPostRedisplay()

    def keyboard(self, key, x, y):
        if key in b"qQ\x1b":
            # sys.exit(0)
            # 不知道为啥上边这个 exit 无法退出程序，改成下面这种方式退出
            os._exit(0)
        elif key in b"1234567":
            self.renderer.set_task(int(key.decode()))
        elif key in b"fF":
            self.renderer.set_shading_mode("flat")
        elif key in b"gG":
            self.renderer.set_shading_mode("gouraud")
        elif key in b"pP":
            self.renderer.set_shading_mode("phong")
        elif key in b"bB":
            self.renderer.toggle_bump()
        elif key in b"iI":
            self.renderer.toggle_shadow()
        elif key in b"+=" or key == GLUT_KEY_UP:
            # 拉近相机
            self.renderer.camera.position.z -= 0.5
            if self.renderer.camera.position.z < 2.0:
                self.renderer.camera.position.z = 2.0
            print(f"相机距离: {self.renderer.camera.position.z:.1f}")
        elif key in b"-_" or key == GLUT_KEY_DOWN:
            # 拉远相机
            self.renderer.camera.position.z += 0.5
            if self.renderer.camera.position.z > 15.0:
                self.renderer.camera.position.z = 15.0
            print(f"相机距离: {self.renderer.camera.position.z:.1f}")
        elif key in b"hH":
            self.print_help()

        glutPostRedisplay()

    def _keyboard_down(self, key, x, y):
        # 委托给之前的 keyboard 函数处理
        if key in b"qQ\x1b1234567fFgGpPbBiI+=-_hH":
            self.keyboard(key, x, y)
            return

        # 实现 ASDW 键前后左右移动 & 空格向上移动
        if key in b"wW":
            self.renderer.camera.moving_forward = True
        elif key in b"sS":
            self.renderer.camera.moving_backward = True
        elif key in b"aA":
            self.renderer.camera.moving_left = True
        elif key in b"dD":
            self.renderer.camera.moving_right = True
        elif key == b" ":
            self.renderer.camera.moving_up = True
        elif key in b"rR":
            self.renderer.camera.reset()
        elif key in b"xX":
            self.renderer.toggle_pause()

        else:
            print(f"未处理的按键: {key}")

        glutPostRedisplay()

    def _keyboard_up(self, key, x, y):
        if key in b"qQ\x1b1234567fFgGpPbBiI+=-_hH":
            return

        if key in b"wW":
            self.renderer.camera.moving_forward = False
        elif key in b"sS":
            self.renderer.camera.moving_backward = False
        elif key in b"aA":
            self.renderer.camera.moving_left = False
        elif key in b"dD":
            self.renderer.camera.moving_right = False
        elif key == b" ":
            self.renderer.camera.moving_up = False
        elif key in b"rR":
            pass
        elif key in b"xX":
            pass

        else:
            print(f"未处理的按键: {key}")

        glutPostRedisplay()

    def _mouse_button(self, button, state, x, y):
        if state == GLUT_DOWN:
            self.is_mouse_down = True
            self.last_mouse_pos = [x, y]
        elif state == GLUT_UP:
            self.is_mouse_down = False

    def _mouse_move(self, x, y):
        if self.is_mouse_down:
            dx, dy = x - self.last_mouse_pos[0], y - self.last_mouse_pos[1]
            self.last_mouse_pos[:] = (x, y)

            if (dx, dy) != (0, 0):
                self.renderer.camera.angle_change(
                    math.radians(dx) / 2, -math.radians(dy) / 2
                )

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


if __name__ == "__main__":
    app = Application()
    app.run()
