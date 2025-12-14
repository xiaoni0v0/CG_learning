#version 430

/*
 * 任务3.2：Gouraud Shading 顶点着色器
 * 
 * 要求：
 * 1. 在顶点着色器中计算Blinn-Phong光照
 * 2. 将计算结果传递到片段着色器进行插值
 * 
 * 提示：
 * - 光照计算与Flat Shading类似
 * - 但使用的是顶点法线，而不是平面法线
 * - 计算结果会在光栅化阶段自动插值
 */

layout(location = 0) in vec4 position;
layout(location = 1) in vec2 texcoord;
layout(location = 2) in vec3 normal;

uniform mat4 MVP;
uniform mat4 M;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform float lightIntensity;

out vec2 vTexCoord;
out vec3 vColor;  // 在顶点着色器计算的颜色

void main() {
    gl_Position = MVP * position;
    
    vColor = vec3(0.75);

}
