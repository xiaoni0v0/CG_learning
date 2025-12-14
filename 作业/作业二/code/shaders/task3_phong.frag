#version 430

/*
 * 任务3.3：Phong Shading 片段着色器
 * 
 * 要求：
 * 1. 在片段着色器中计算Blinn-Phong光照
 * 2. 使用插值后的法线
 * 
 * 提示：
 * - 与Flat Shading类似，但使用插值后的顶点法线
 * - 需要重新归一化插值后的法线
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

// 材料属性
uniform float ka;
uniform float kd;
uniform float ks;
uniform float shininess;

void main() {
    // 法线 N
    vec3 N = normalize(vNormal);
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
