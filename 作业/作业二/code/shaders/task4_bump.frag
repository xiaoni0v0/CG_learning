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

void main() {

	vec3 color = vec3(0.75);
    FragColor = vec4(color, 1.0);
}
