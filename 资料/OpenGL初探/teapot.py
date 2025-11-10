# -*- coding: utf-8 -*-
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

transformation = "null"

pos = [0, 0, 14]


def init():
    """Initialize OpenGL settings"""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glEnable(GL_DEPTH_TEST)  # Enable depth testing

    # Set up lighting (optional but makes the teapot look better)
    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    # glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 1, 0])
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])


def set_projection():
    """Set up the projection matrix as specified"""
    print("set_projection")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Set up the frustum with the parameters from the image:
    # left=-4, right=4, bottom=-3, top=3, near=5, far=80
    glFrustum(-4, 4, -3, 3, 5, 80)
    # glOrtho(-4, 4, -3, 3, 5, 80)

    print(glGetDoublev(GL_PROJECTION_MATRIX).T)

    # The resulting projection matrix should be:

    # [  2/(r-l)     0         0       -(r+l)/(r-l)    ]
    # [     0     2/(t-b)      0       -(t+b)/(t-b)    ]
    # [     0        0     -2/(f-n)    -(f+n)/(f-n)    ]
    # [     0        0         0             1         ]

    # [  2/(r-l)     0         0       -(r+l)/(r-l)    ]     [    n    0    0    0    ]
    # [     0     2/(t-b)      0       -(t+b)/(t-b)    ]  *  [    0    n    0    0    ]
    # [     0        0     -2/(f-n)    -(f+n)/(f-n)    ]     [    0    0   n+f   nf   ]
    # [     0        0         0             1         ]     [    0    0   -1    0    ]

    # [1.25    0       0        0      ]
    # [0       1.667   0        0      ]
    # [0       0      -1.1333  -10.667 ]
    # [0       0      -1        0      ]

    A = np.array(
        [[1 / 4, 0, 0, 0], [0, 1 / 3, 0, 0], [0, 0, -2 / 75, -85 / 75], [0, 0, 0, 1]]
    )
    B = np.array([[5, 0, 0, 0], [0, 5, 0, 0], [0, 0, 85, 400], [0, 0, -1, 0]])

    print()
    # print(A)
    print(A @ B)


def set_modelview():
    """Set up the modelview matrix as specified"""
    print("set_modelview")

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Translate to position the camera at (0, 0, 14)
    # This is equivalent to moving the scene to (0, 0, -14)
    # glTranslatef(0, 0, -14)
    gluLookAt(*pos, 0, 0, 0, 0, 1, 0)

    # print(glGetDoublev(GL_MODELVIEW_MATRIX).T)

    # The resulting modelview matrix should be:
    # [1  0  0   0  ]
    # [0  1  0   0  ]
    # [0  0  1  -14 ]
    # [0  0  0   1  ]


def draw_wireframe_cube():
    """Draw a red wireframe cube with size 6"""
    glColor3f(1, 0, 0)  # Red color
    glutWireCube(6)


def draw_teapot():
    """Draw a blue solid teapot with size 2.0"""
    global transformation
    # print(transformation)
    glColor3f(0, 0, 1)  # Blue color
    glPushMatrix()
    if transformation == "translate":
        glTranslatef(1.5, -0.5, 0)
    elif transformation == "scale":
        glScalef(1.5, 1.0, 1.5)
    elif transformation == "rotate":
        glRotatef(30, 1, 1, 1)
    glutSolidTeapot(2.0)
    glPopMatrix()


def display():
    """Main display function"""
    print("display")

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 清除颜色缓冲区和深度缓冲区

    # MV 矩阵
    set_modelview()

    # 画一个大小为 6 的红色的线框立方体
    draw_wireframe_cube()

    # 在线框内部画一个茶壶
    draw_teapot()

    glutSwapBuffers()


def reshape(width, height):
    """Handle window reshape"""
    # print("reshape")
    #
    # glViewport(0, 0, width, height)
    # set_projection()


def keyboard(key, x, y):
    """Handle keyboard input"""
    print("keyboard")

    global transformation

    match key:
        case b"\x1b":  # ESC
            print("ESCAPE")
            glutLeaveMainLoop()  # 或者使用 sys.exit()
        case b"1":
            transformation = "translate"
            print("Mode: Translate")
        case b"2":
            transformation = "scale"
            print("Mode: Scale")
        case b"3":
            transformation = "rotate"
            print("Mode: Rotate")
        case b" ":  # Space key
            transformation = "null"
            print("Mode: Null")

        # 移动摄像机
        # WASD 分别对应前左后右
        # QE 分别对应下上
        case b"w":
            pos[2] -= 1
        case b"s":
            pos[2] += 1
        case b"a":
            pos[0] -= 1
        case b"d":
            pos[0] += 1
        case b"q":
            pos[1] -= 1
        case b"e":
            pos[1] += 1

    glutPostRedisplay()


def main():
    """Main function"""
    # 初始化 GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Teapot in a Wireframe Cube")

    # 设置回调函数
    glutDisplayFunc(display)  # 显示时调用的函数
    glutReshapeFunc(reshape)  # 窗口大小改变时调用的函数
    glutKeyboardFunc(keyboard)  # 键盘按下时调用的函数

    # 初始化 OpenGL
    init()
    set_projection()

    # 进入 GLUT 主循环
    glutMainLoop()


if __name__ == "__main__":
    main()
