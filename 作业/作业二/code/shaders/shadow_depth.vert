#version 430

/*
 * 阴影深度顶点着色器（框架提供，无需修改）
 */

layout(location = 0) in vec4 position;

uniform mat4 lightSpaceMatrix;

void main() {
    gl_Position = lightSpaceMatrix * position;
}
