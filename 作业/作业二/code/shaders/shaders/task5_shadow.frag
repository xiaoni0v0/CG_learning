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

in vec2 vTexCoord;
in vec3 vNormal;
in vec3 vWorldPos;
in vec4 vLightSpacePos;

uniform sampler2D texDiffuse;
uniform sampler2D shadowMap;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform float lightIntensity;

out vec4 FragColor;

void main() {
    
	vec3 color = vec3(0.75);
    FragColor = vec4(color, 1.0);
}
