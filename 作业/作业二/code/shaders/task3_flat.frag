#version 430

/*
 * 任务3.1：Flat Shading
 * 
 * 要求：
 * 1. 使用dFdx和dFdy计算平面法线（每个三角形一个法线）
 * 2. 实现Blinn-Phong光照模型
 * 
 * Blinn-Phong模型：
 * - 环境光：ambient = ka * lightColor
 * - 漫反射：diffuse = kd * lightColor * max(dot(N, L), 0) / r^2
 * - 镜面反射：specular = ks * lightColor * pow(max(dot(N, H), 0), shininess) / r^2
 * 
 * 其中：
 * - N: 法线
 * - L: 光源方向
 * - V: 视线方向
 * - H: 半程向量 = normalize(L + V)
 * - r: 光源距离
 * 
 * 提示：
 * - 使用dFdx(vWorldPos)和dFdy(vWorldPos)计算三角形边
 * - 法线 = normalize(cross(edge1, edge2))
 */

in vec2 vTexCoord; // 顶点的纹理坐标
in vec3 vNormal;   // 顶点处的法向量
in vec3 vWorldPos; // 顶点的世界坐标

uniform sampler2D texDiffuse; // 纹理贴图
uniform vec3 lightPos;        // 光源位置
uniform vec3 viewPos;         // 视点位置
uniform vec3 lightColor;      // 光源颜色
uniform float lightIntensity; // 光源强度

out vec4 FragColor; // 输出，当前片元的颜色

// 材料属性
uniform float ka;
uniform float kd;
uniform float ks;
uniform float shininess;

void main() {
    // 法线 N
    vec3 N = normalize(cross(dFdx(vWorldPos), dFdy(vWorldPos)));
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

    FragColor = vec4(
    texture(texDiffuse, vTexCoord).rgb * (ambient + diffuse + specular) * lightIntensity,
    1);
}
