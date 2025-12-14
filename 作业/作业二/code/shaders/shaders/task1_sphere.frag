#version 430

/*
 * 任务1：纹理采样片段着色器
 * 
 * 要求：
 * 1. 从纹理中采样颜色
 * 2. 输出到gl_FragColor
 * 
 * 提示：
 * - 使用texture()函数进行纹理采样
 * - 采样器类型为sampler2D
 */

in vec2 vTexCoord;

uniform sampler2D texDiffuse;

out vec4 FragColor;

void main() {


    vec3 color = vec3(0.75);
    FragColor = vec4(color, 1.0);
}
