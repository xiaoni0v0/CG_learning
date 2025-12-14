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

in vec2 vTexCoord;
in vec3 vNormal;
in vec3 vWorldPos;

uniform sampler2D texDiffuse;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform float lightIntensity;

out vec4 FragColor;

void main() {

	vec3 color = vec3(0.75);
    FragColor = vec4(color, 1.0);
}
