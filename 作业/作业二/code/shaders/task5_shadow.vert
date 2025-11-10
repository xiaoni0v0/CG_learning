#version 430

/*
 * 任务5：阴影顶点着色器（框架提供，学生无需修改）
 */

layout(location = 0) in vec4 position;
layout(location = 1) in vec2 texcoord;
layout(location = 2) in vec3 normal;

uniform mat4 MVP;
uniform mat4 M;
uniform mat4 lightSpaceMatrix;

out vec2 vTexCoord;
out vec3 vNormal;
out vec3 vWorldPos;
out vec4 vLightSpacePos;

void main() {
    gl_Position = MVP * position;
    vTexCoord = texcoord;
    vNormal = mat3(M) * normal;
    vWorldPos = (M * position).xyz;
    vLightSpacePos = lightSpaceMatrix * M * position;
}
