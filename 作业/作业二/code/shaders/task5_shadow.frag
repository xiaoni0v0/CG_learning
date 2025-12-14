#version 430

/*
 * 任务5：阴影贴图
 *
 * 要求：
 * 1. 使用阴影贴图判断片段是否在阴影中
 * 2. 实现PCF（Percentage Closer Filtering）软阴影
 *
 * 原理：
 * - 从光源视角渲染场景，记录深度到阴影贴图
 * - 在正常渲染时，将片段位置变换到光源空间
 * - 比较片段深度与阴影贴图中的深度
 * - 如果片段深度大于阴影贴图深度，说明在阴影中
 *
 * PCF软阴影：
 * - 对阴影贴图周围多个位置采样
 * - 计算在阴影中的比例
 * - 使阴影边缘更加柔和
 *
 * 提示：
 * - 光源空间坐标已通过vLightSpacePos传入
 * - 需要进行透视除法：pos.xyz / pos.w
 * - 将[-1,1]范围映射到[0,1]纹理坐标
 * - 添加bias避免阴影失真（shadow acne）
 */

in vec2 vTexCoord;      // 顶点的纹理坐标
in vec3 vNormal;        // 顶点处的法向量
in vec3 vWorldPos;      // 顶点的世界坐标
in vec4 vLightSpacePos; // 顶点在光源系下的位置

uniform sampler2D texDiffuse; // 材质贴图
uniform sampler2D shadowMap;  // 阴影贴图
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

float sampleIfShadow(vec4);
float PCF(vec4);

void main() {
    float shadow = PCF(vLightSpacePos);

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
    texture(texDiffuse, vTexCoord).rgb * (ambient + (diffuse + specular) * (1.0 - shadow)) * lightIntensity,
    1);
}

// 根据阴影贴图判断是否在阴影中。采样一次
float sampleIfShadow(vec4 pos) {
    vec3 shadowCoord = pos.xyz / pos.w * 0.5 + 0.5; // 透视除法 & 从 [-1,1] 变换到 [0,1]
    float closestDepth = texture(shadowMap, shadowCoord .xy).r; // 从阴影贴图中采样深度（最小的深度）
    float currentDepth = shadowCoord .z;                        // 片元在光源空间下的深度
    return currentDepth - 0.02 > closestDepth ? 1.0 : 0.0;
}

// 计算PCF软阴影。采样多次
float PCF(vec4 pos) {
    float shadow = 0.0;
    int nSamples = 0;

    float radius = 0.02;
    float step = radius / 10.0;

    for (float i = -radius; i <= radius; i += step) {
        for (float j = -radius; j <= radius; j += step) {
            shadow += sampleIfShadow(pos + vec4(i, j, 0, 0));
            nSamples++;
        }
    }

    return shadow / nSamples;
}
