#version 430

/*
 * 任务3.2：Gouraud Shading 片段着色器
 * 
 * 要求：
 * 1. 使用顶点着色器计算的光照颜色
 * 2. 与纹理颜色相乘
 */

in vec2 vTexCoord;
in vec3 vColor;

uniform sampler2D texDiffuse;

out vec4 FragColor;

void main() {
    FragColor = vec4(vColor, 1.0);
}
