
import numpy as np
from PIL import Image
from OpenGL.GL import *


def load_texture(path, mipmap=True, use_linear=True):
    """加载纹理"""
    texture = glGenTextures(1)
    
    try:
        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(img, dtype=np.uint8)
        
        glBindTexture(GL_TEXTURE_2D, texture)
        
        if img.mode == 'RGB':
            format_type = GL_RGB
        elif img.mode == 'RGBA':
            format_type = GL_RGBA
        else:
            img = img.convert('RGB')
            img_data = np.array(img, dtype=np.uint8)
            format_type = GL_RGB
        
        
        glTexImage2D(GL_TEXTURE_2D, 0, format_type, 
                     img.width, img.height, 0, 
                     format_type, GL_UNSIGNED_BYTE, img_data)
                     
        
        if mipmap:
            glGenerateMipmap(GL_TEXTURE_2D)
            if use_linear:
                # 三线性过滤（最平滑）
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            else:
                # 最近邻过滤（会产生锯齿）
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        else:
            if use_linear:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            else:
                # 最近邻过滤（会产生明显锯齿）
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
          
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        #if mipmap and use_linear:
        #    max_anisotropy = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
        #    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, max_anisotropy)
        
        return texture
        
    except Exception as e:
        print(f"加载纹理失败 {path}: {e}")
        return 0

def load_texture_no_filter(path):
    """加载纹理（无过滤，用于演示锯齿）"""
    return load_texture(path, mipmap=False, use_linear=False)


def load_texture_with_mipmap(path):
    """加载纹理（带 mipmap 和三线性过滤）"""
    return load_texture(path, mipmap=True, use_linear=True)