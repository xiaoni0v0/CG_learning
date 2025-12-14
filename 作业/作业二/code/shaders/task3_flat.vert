#version 430

/*
 * 任务1：球面顶点着色器
 * 
 * 要求：
 * 1. 正确变换顶点位置到裁剪空间
 * 2. 传递纹理坐标到片段着色器
 * 
 * 提示：
 * - 使用MVP矩阵进行顶点变换
 * - 纹理坐标直接传递即可
 */

layout (location = 0) in vec4 position;
layout (location = 1) in vec2 texcoord;
layout (location = 2) in vec3 normal;

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
