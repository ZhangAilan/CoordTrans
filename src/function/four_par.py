import numpy as np
from typing import List, Tuple, Dict

def calculate_four_parameters(
    source_points: List[Tuple[float, float]], 
    target_points: List[Tuple[float, float]]
) -> Dict[str, float]:
    """
    计算二维坐标系统之间的四参数转换参数。
    
    参数:
        source_points: 源坐标系中的坐标点列表，每个元素为 (x, y) 坐标元组
        target_points: 目标坐标系中的对应坐标点列表，每个元素为 (X, Y) 坐标元组
        
    返回:
        包含四个参数的字典:
            - 'a': 缩放旋转参数 a = s·cos(θ)
            - 'b': 缩放旋转参数 b = s·sin(θ)
            - 'dx': X方向平移参数
            - 'dy': Y方向平移参数
            - 's': 尺度因子
            - 'theta': 旋转角度（弧度）
    
    注意:
        至少需要两个控制点才能计算四参数
    """
    # 检查输入点数量
    if len(source_points) < 2 or len(target_points) < 2:
        raise ValueError("至少需要两个控制点来计算四参数转换")
    
    if len(source_points) != len(target_points):
        raise ValueError("源坐标点和目标坐标点数量必须相等")
    
    # 构建最小二乘方程组
    n = len(source_points)
    A = np.zeros((2*n, 4))
    L = np.zeros(2*n)
    
    for i in range(n):
        x, y = source_points[i]
        X, Y = target_points[i]
        
        # 构建A矩阵
        A[2*i, 0] = x
        A[2*i, 1] = -y
        A[2*i, 2] = 1
        A[2*i, 3] = 0
        
        A[2*i+1, 0] = y
        A[2*i+1, 1] = x
        A[2*i+1, 2] = 0
        A[2*i+1, 3] = 1
        
        # 构建L矩阵
        L[2*i] = X
        L[2*i+1] = Y
    
    # 解最小二乘方程组: A * X = L
    X, residuals, rank, s = np.linalg.lstsq(A, L, rcond=None)
    
    # 提取参数
    a, b, dx, dy = X
    
    # 计算尺度因子和旋转角度
    scale = np.sqrt(a**2 + b**2)
    theta = np.arctan2(b, a)
    
    return {
        'a': a,
        'b': b,
        'dx': dx,
        'dy': dy,
        's': scale,
        'theta': theta
    }

def transform_coordinates(
    points: List[Tuple[float, float]], 
    params: Dict[str, float]
) -> List[Tuple[float, float]]:
    """
    使用四参数模型将坐标从源坐标系转换到目标坐标系。
    
    参数:
        points: 源坐标系中需要转换的点列表，每个元素为 (x, y) 坐标元组
        params: 包含四参数转换参数的字典 ('a', 'b', 'dx', 'dy')
        
    返回:
        转换后的坐标点列表，每个元素为 (X, Y) 坐标元组
    """
    a = params['a']
    b = params['b']
    dx = params['dx']
    dy = params['dy']
    
    transformed_points = []
    for x, y in points:
        X = a * x - b * y + dx
        Y = b * x + a * y + dy
        transformed_points.append((X, Y))
    
    return transformed_points

def transform_point_four_par(point, params):
    """
    使用四参数模型转换单点坐标
    
    参数:
    point: Tuple[float, float] 或 numpy.ndarray
        源坐标系中的点坐标，格式为 (x, y)
    params: Dict[str, float] 或包含四个元素的序列
        四参数 {'a': float, 'b': float, 'dx': float, 'dy': float} 或
        [a, b, dx, dy]
        
    返回:
    Tuple[float, float]
        目标坐标系中的点坐标 (X, Y)
    """
    # 处理参数输入
    if isinstance(params, dict):
        a = params['a']
        b = params['b']
        dx = params['dx']
        dy = params['dy']
    else:
        a, b, dx, dy = params
        
    # 获取输入点坐标
    if hasattr(point, '__len__') and len(point) == 2:
        x, y = point
    else:
        raise ValueError("输入点坐标应为包含2个元素的序列 (x, y)")
    
    # 应用四参数转换
    X = a * x - b * y + dx
    Y = b * x + a * y + dy
    
    return (X, Y)

