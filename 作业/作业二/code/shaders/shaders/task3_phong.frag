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

void main() {
	vec3 color = vec3(0.75);
    FragColor = vec4(color, 1.0);
}
