#version 430

in vec2 vTexCoord;      // 顶点的纹理坐标
in vec3 vNormal;        // 顶点处的法向量
in vec3 vWorldPos;      // 顶点的世界坐标

uniform sampler2D texDiffuse; // 材质贴图
uniform vec3 lightPos;        // 光源位置
uniform vec3 viewPos;         // 相机位置
uniform vec3 lightColor;      // 光源颜色
uniform float lightIntensity; // 光源强度

out vec4 FragColor;

// 材料属性
uniform float ka;
uniform float kd;
uniform float ks;
uniform float shininess;
uniform int isSkybox;

// 将3D方向向量转换为2D球面映射纹理坐标
vec2 directionToSphericalUV(vec3 dir) {
    const float PI = acos(-1.0);
    float phi = atan(dir.z, dir.x); // 方位角，∈ [-π, π]
    float theta = asin(dir.y);      // 仰角，∈ [-π/2, π/2]
    // 将角度转换到 [0, 1] 范围
    float u = phi / (2.0 * PI) + 0.5;
    float v = theta / PI + 0.5;
    return vec2(u, v);
}

void main() {
    // 处理天空盒
    if (isSkybox == 1) {
        FragColor = vec4(texture(texDiffuse, vTexCoord).rgb, 1);
        return;
    }

    vec3 N = normalize(vNormal);              // 法线 N
    vec3 L = normalize(lightPos - vWorldPos); // 光源方向 L
    vec3 V = normalize(viewPos - vWorldPos);  // 视线方向 V
    vec3 H = normalize(L + V);                // 半程向量 H
    float r = length(lightPos - vWorldPos);   // 光源距离 r

    // 反射向量 R
    vec3 R = normalize(reflect(-V, N));
    // 采样环境颜色
    vec2 envUV = directionToSphericalUV(R);
    // vec3 reflectColor = texture(texDiffuse, envUV).rgb;
    // reflectColor 要算一个平均，形成模糊的效果
    vec3 reflectColor = vec3(0);
    int nSamples = 0;
    float radius = 0.01;
    float step = radius / 5.0;
    for (float i = -radius; i <= radius; i += step) {
        for (float j = -radius; j <= radius; j += step) {
            reflectColor += texture(texDiffuse, envUV + vec2(i, j)).rgb;
            nSamples++;
        }
    }
    reflectColor /= nSamples;

    vec3 color = mix(
        vec3(0, 128, 128) / 255.0, // 青色
        reflectColor,
        0.1
    );

    // 带入 Blinn-Phong 模型
    vec3 ambient = ka * lightColor;
    vec3 diffuse = kd * lightColor * max(dot(N, L), 0) / (r * r);
    vec3 specular = ks * lightColor * pow(max(dot(N, H), 0), shininess) / (r * r);

    FragColor = vec4(
    color * (ambient + diffuse + specular) * lightIntensity,
    1);
}
