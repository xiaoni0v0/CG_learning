import numpy as np


def create_sphere(radius=1.0, slices=64, stacks=32):
    """
    生成球面三角化数据
    返回: positions, texcoords, normals
    """
    vertices = []
    
    for i in range(stacks + 1):
        theta = i * np.pi / stacks
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        
        for j in range(slices + 1):
            phi = j * 2 * np.pi / slices
            sin_phi = np.sin(phi)
            cos_phi = np.cos(phi)
            
            x = radius * sin_theta * cos_phi
            y = radius * cos_theta
            z = radius * sin_theta * sin_phi
            
            u = j / slices
            v = i / stacks
            
            nx = sin_theta * cos_phi
            ny = cos_theta
            nz = sin_theta * sin_phi
            
            vertices.append([x, y, z, 1.0, u, v, nx, ny, nz])
    
    vertices = np.array(vertices, dtype=np.float32)
    
    indices = []
    for i in range(stacks):
        for j in range(slices):
            first = i * (slices + 1) + j
            second = first + slices + 1
            
            indices.extend([first, second, first + 1])
            indices.extend([second, second + 1, first + 1])
    
    indices = np.array(indices, dtype=np.uint32)
    indexed_vertices = vertices[indices]
    
    positions = indexed_vertices[:, 0:4]
    texcoords = indexed_vertices[:, 4:6]
    normals = indexed_vertices[:, 6:9]
    
    return positions, texcoords, normals


def create_plane(size=5.0):
    """生成地面平面"""
    vertices = np.array([
        [-size, 0.0, -size, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [ size, 0.0, -size, 1.0, 5.0, 0.0, 0.0, 1.0, 0.0],
        [ size, 0.0,  size, 1.0, 5.0, 5.0, 0.0, 1.0, 0.0],
        [-size, 0.0, -size, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [ size, 0.0,  size, 1.0, 5.0, 5.0, 0.0, 1.0, 0.0],
        [-size, 0.0,  size, 1.0, 0.0, 5.0, 0.0, 1.0, 0.0],
    ], dtype=np.float32)
    
    positions = vertices[:, 0:4]
    texcoords = vertices[:, 4:6]
    normals = vertices[:, 6:9]
    
    return positions, texcoords, normals
