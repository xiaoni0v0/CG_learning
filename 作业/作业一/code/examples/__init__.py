"""
示例模块
"""

from .basic_rendering import basic_triangle_example
from .projection_demo import projection_comparison_example
from .antialiasing_demo import antialiasing_comparison_example
from .depth_test_demo import depth_test_example
from .rotation_demo import rotation_interpolation_example

__all__ = [
    'basic_triangle_example',
    'projection_comparison_example', 
    'antialiasing_comparison_example',
    'depth_test_example',
    'rotation_interpolation_example'
]
