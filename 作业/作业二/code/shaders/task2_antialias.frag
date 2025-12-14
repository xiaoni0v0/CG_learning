#version 430

/*
 * 任务2：纹理反走样
 * 
 * 要求：
 * 1. 实现纹理的反走样处理
 * 2. 对比GL_NEAREST和GL_LINEAR的效果
 * 
 * 方法1：使用Mipmap（推荐）
 * - 通过textureGrad()或texture()自动选择mipmap层级
 * 
 * 方法2：手动多重采样
 * - 对纹理坐标周围进行多次采样并平均
 * 
 * 提示：
 * - Mipmap已在纹理加载时生成
 * - 可以使用textureQueryLod()查询mipmap层级
 */

in vec2 vTexCoord;

uniform sampler2D texDiffuse;

out vec4 FragColor;

void main() {

    // vec3 color = vec3(0.75);
    // FragColor = vec4(color, 1.0);

    FragColor = texture(texDiffuse, vTexCoord);

}
