import numpy as np

def bursa_seven_parameters(source_coords, target_coords):
    """
    计算布尔莎七参数转换参数及精度评估
    
    参数:
    source_coords: numpy.ndarray, shape (n,3)
        源坐标系中的坐标点列表，必须是空间直角坐标系(XYZ)格式
    target_coords: numpy.ndarray, shape (n,3)
        目标坐标系中的坐标点列表，必须是空间直角坐标系(XYZ)格式
    
    返回:
    dict: 包含以下键值:
        'parameters': numpy.ndarray, shape (7,)
            七参数 [ΔX₀, ΔY₀, ΔZ₀, εx, εy, εz, m]
        'residuals': numpy.ndarray, shape (n,3)
            残差 [X误差, Y误差, Z误差]
        'rms': float
            中误差
        'stats': dict
            包含每个方向的统计信息 {
                'x_stats': [min, max, mean, std],
                'y_stats': [min, max, mean, std],
                'z_stats': [min, max, mean, std]
            }
    """
    # 1. 确保输入数据是numpy数组且形状正确
    source = np.array(source_coords)
    target = np.array(target_coords)
    
    if source.shape != target.shape or len(source.shape) != 2 or source.shape[1] != 3:
        raise ValueError("输入坐标数组格式不正确，应为(n,3)的数组")
    
    n_points = source.shape[0]
    if n_points < 3:
        raise ValueError("至少需要3个公共点进行七参数转换")

    # 2. 构建系数矩阵B和观测向量L
    B = np.zeros((n_points * 3, 7))
    L = np.zeros(n_points * 3)
    
    for i in range(n_points):
        # 构建每个点的系数矩阵
        B[i*3:i*3+3, 0:3] = np.eye(3)  # ΔX₀, ΔY₀, ΔZ₀的系数
        B[i*3:i*3+3, 3] = [0, -source[i,2], source[i,1]]  # εx的系数
        B[i*3:i*3+3, 4] = [source[i,2], 0, -source[i,0]]  # εy的系数
        B[i*3:i*3+3, 5] = [-source[i,1], source[i,0], 0]  # εz的系数
        B[i*3:i*3+3, 6] = source[i]  # m的系数
        
        # 构建观测向量
        L[i*3:i*3+3] = target[i] - source[i]

    # 3. 最小二乘解算
    N = B.T @ B
    W = B.T @ L
    parameters = np.linalg.solve(N, W)

    # 4. 计算残差
    V = B @ parameters - L
    residuals = V.reshape(-1, 3)
    
    # 5. 计算中误差
    v_v = V.T @ V
    sigma0 = np.sqrt(v_v / (3 * n_points - 7))
    
    # 6. 计算统计信息
    stats = {
        'x_stats': [np.min(residuals[:,0]), np.max(residuals[:,0]), 
                   np.mean(residuals[:,0]), np.std(residuals[:,0])],
        'y_stats': [np.min(residuals[:,1]), np.max(residuals[:,1]),
                   np.mean(residuals[:,1]), np.std(residuals[:,1])],
        'z_stats': [np.min(residuals[:,2]), np.max(residuals[:,2]),
                   np.mean(residuals[:,2]), np.std(residuals[:,2])]
    }

    return {
        'parameters': parameters,
        'residuals': residuals,
        'rms': sigma0,
        'stats': stats
    }

def transform_point_seven_par(point, parameters):
    """
    使用七参数转换单点的空间直角坐标
    
    参数:
    point: numpy.ndarray, shape (3,)
        源坐标系中的坐标点，必须是空间直角坐标系(XYZ)格式
    parameters: numpy.ndarray, shape (7,)
        七参数 [ΔX₀, ΔY₀, ΔZ₀, εx, εy, εz, m]
    
    返回:
    numpy.ndarray, shape (3,)
        目标坐标系中的坐标点
    """
    # 确保输入是numpy数组
    point = np.array(point)
    if point.shape != (3,):
        raise ValueError("输入点坐标应为包含3个元素的数组")
    
    # 提取参数
    dx, dy, dz = parameters[0:3]  # 平移参数
    ex, ey, ez = parameters[3:6]  # 旋转参数
    m = parameters[6]  # 尺度因子
    
    # 构建旋转矩阵
    R = np.array([
        [1, -ez, ey],
        [ez, 1, -ex],
        [-ey, ex, 1]
    ])
    
    # 应用七参数转换
    # X' = X₀ + (1+m)·R·X
    transformed_point = np.array([dx, dy, dz]) + (1 + m) * (R @ point)
    
    return transformed_point
