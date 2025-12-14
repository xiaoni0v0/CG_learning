#version 430

/*
 * 任务3.3：Phong Shading 顶点着色器
 * 
 * 要求：
 * 1. 传递必要的数据到片段着色器
 * 2. 光照计算在片段着色器中进行
 */

layout(location = 0) in vec4 position;
layout(location = 1) in vec2 texcoord;
layout(location = 2) in vec3 normal;

uniform mat4 MVP;
uniform mat4 M;

out vec2 vTexCoord;
out vec3 vNormal;
out vec3 vWorldPos;

void main() {

    gl_Position = MVP * position;
    vTexCoord = texcoord;
    vNormal = mat3(M) * normal;
    vWorldPos = (M * position).xyz;
}
