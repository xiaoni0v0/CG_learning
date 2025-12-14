#version 430

/*
 * 任务4：Bump Mapping
 * 
 * 要求：
 * 1. 从bump贴图读取高度信息
 * 2. 计算切线空间的法线扰动
 * 3. 将扰动后的法线用于光照计算
 * 
 * 提示：
 * - 使用dFdx和dFdy计算切线和副切线
 * - bump强度可以通过uniform控制
 */

in vec2 vTexCoord;
in vec3 vNormal;
in vec3 vWorldPos;

uniform sampler2D texDiffuse;
uniform sampler2D texBump;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform float lightIntensity;
uniform float bumpStrength;

out vec4 FragColor;

// 材料属性
uniform float ka;
uniform float kd;
uniform float ks;
uniform float shininess;

void main() {
    // 法线 N
    vec3 N = normalize(vNormal);
    float B = texture(texBump, vTexCoord).r;
    vec3 P = vWorldPos;
    N = normalize(
        N
        + bumpStrength * (
        dFdx(B) * normalize(dFdx(P))
        +
        dFdy(B) * normalize(dFdy(P))
        )
    );

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
