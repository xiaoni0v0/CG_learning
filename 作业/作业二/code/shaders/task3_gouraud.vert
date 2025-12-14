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

layout (location = 0) in vec4 position;
layout (location = 1) in vec2 texcoord;
layout (location = 2) in vec3 normal;

uniform mat4 MVP;
uniform mat4 M;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform float lightIntensity;

out vec2 vTexCoord;
out vec3 vColor;  // 在顶点着色器计算的颜色

// 材料属性
uniform float ka;
uniform float kd;
uniform float ks;
uniform float shininess;

void main() {
    gl_Position = MVP * position;
    vTexCoord = texcoord;

    // 顶点的世界坐标 vWorldPos
    vec3 vWorldPos = (M * position).xyz;

    // 法线 N
    vec3 N = normalize(mat3(transpose(inverse(M))) * normal);
    // 光源方向 L
    vec3 L = normalize(lightPos - vWorldPos);
    // 视线方向 V
    vec3 V = normalize(viewPos - vWorldPos);
    // 半程向量 H
    vec3 H = normalize(L + V);
    // 光源距离 r
    float r = length(lightPos - vWorldPos);

    // 带入 Blinn-Phong 模型
    vec3 ambient = ka * lightColor;
    vec3 diffuse = kd * lightColor * max(dot(N, L), 0) / (r * r);
    vec3 specular = ks * lightColor * pow(max(dot(N, H), 0), shininess) / (r * r);

    vColor = (ambient + diffuse + specular) * lightIntensity;
}
