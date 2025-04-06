import numpy as np

def Beijing54_BLH2XYZ(B, L, H):
    """
    Beijing54坐标系下BLH到XYZ的转换
    
    参数:
    B: float, 大地纬度(弧度)
    L: float, 大地经度(弧度)
    H: float, 大地高(米)
    
    返回:
    tuple: (X, Y, Z) 地心地固直角坐标
    """
    # Beijing54椭球参数
    a = 6378245.0  # 长半轴
    f = 1/298.3  # 扁率
    e2 = 2*f - f*f  # 第一偏心率平方
    
    # 计算卯酉圈曲率半径N
    N = a / np.sqrt(1 - e2 * np.sin(B)**2)
    
    # 计算X、Y、Z
    X = (N + H) * np.cos(B) * np.cos(L)
    Y = (N + H) * np.cos(B) * np.sin(L)
    Z = (N * (1 - e2) + H) * np.sin(B)
    
    return X, Y, Z

def Beijing54_XYZ2BLH(X, Y, Z):
    """
    Beijing54坐标系下XYZ到BLH的转换
    
    参数:
    X: float, 地心地固直角坐标X(米)
    Y: float, 地心地固直角坐标Y(米)
    Z: float, 地心地固直角坐标Z(米)
    
    返回:
    tuple: (B, L, H) 大地纬度(弧度)、大地经度(弧度)、大地高(米)
    """
    # Beijing54椭球参数
    a = 6378245.0  # 长半轴
    f = 1/298.3  # 扁率
    e2 = 2*f - f*f  # 第一偏心率平方
    eps = 1e-12  # 迭代精度阈值
    
    # 计算大地经度L
    L = np.arctan2(Y, X)
    
    # 计算辅助参数
    p = np.sqrt(X**2 + Y**2)
    
    # 初始化大地纬度B的计算
    B = np.arctan2(Z, p*(1-e2))  # 初始值
    
    # 迭代计算大地纬度B
    while True:
        N = a / np.sqrt(1 - e2*np.sin(B)**2)
        H = p/np.cos(B) - N
        B_new = np.arctan2(Z + e2*N*np.sin(B), p)
        
        # 检查收敛条件
        if np.abs(B_new - B) < eps:
            B = B_new
            break
        
        B = B_new
    
    # 最终计算大地高H
    N = a / np.sqrt(1 - e2*np.sin(B)**2)
    H = p/np.cos(B) - N
    
    return B, L, H

def Beijing54_BLH2xy(B, L, central_meridian=None, degree_belt=6, false_easting=500000, false_northing=0):
    """
    北京54坐标系下大地坐标(BLH)转高斯投影平面坐标(x,y)
    
    参数:
    B: float, 大地纬度(弧度)
    L: float, 大地经度(弧度)
    central_meridian: float, 中央经线(弧度)，如果为None则自动根据degree_belt计算
    degree_belt: int, 投影带宽，3度带或6度带
    false_easting: float, 东偏移(默认500000米)
    false_northing: float, 北偏移(默认0米)
    
    返回:
    tuple: (x, y) 高斯投影坐标，x为东坐标，y为北坐标(米)
    """
    # 北京54椭球参数
    a = 6378245.0  # 长半轴
    f = 1/298.3  # 扁率
    e2 = 2*f - f*f  # 第一偏心率平方
    e_prime2 = e2/(1-e2)  # 第二偏心率平方
    
    # 确定中央经线
    if central_meridian is None:
        # 确定带号
        if degree_belt == 3:
            # 3度带
            zone_number = int(L * 180 / np.pi / 3) + 1
            central_meridian = (zone_number * 3 - 1.5) * np.pi / 180
        else:
            # 6度带
            zone_number = int(L * 180 / np.pi / 6) + 1
            central_meridian = (zone_number * 6 - 3) * np.pi / 180
    
    # 计算经差l
    l = L - central_meridian
    
    # 计算辅助参数
    sin_B = np.sin(B)
    cos_B = np.cos(B)
    tan_B = np.tan(B)
    
    N = a / np.sqrt(1 - e2 * sin_B**2)  # 卯酉圈曲率半径
    
    t = tan_B
    eta2 = e_prime2 * cos_B**2
    
    # 计算高斯投影坐标
    X = a * (1 - e2) * (
        (1 + 3*e2/4 + 45*e2**2/64 + 175*e2**3/256 + 11025*e2**4/16384) * B
        - (3*e2/8 + 15*e2**2/32 + 525*e2**3/1024 + 2205*e2**4/4096) * np.sin(2*B)
        + (15*e2**2/256 + 105*e2**3/1024 + 2205*e2**4/16384) * np.sin(4*B)
        - (35*e2**3/3072 + 315*e2**4/12288) * np.sin(6*B)
        + (315*e2**4/131072) * np.sin(8*B)
    )
    
    x = X + N * sin_B * cos_B * l**2 * (1/2 + (5 - t**2 + 9*eta2 + 4*eta2**2)/24 * l**2 + (61 - 58*t**2 + t**4)/720 * l**4)
    y = N * l * cos_B * (1 + (1 - t**2 + eta2)/6 * l**2 + (5 - 18*t**2 + t**4 + 14*eta2 - 58*eta2*t**2)/120 * l**4)
    
    # 添加偏移量
    y = y + false_easting
    x = x + false_northing
    
    return y, x  # 注意：x为东坐标，y为北坐标

def Beijing54_xy2BLH(x, y, central_meridian=None, degree_belt=6, false_easting=500000, false_northing=0):
    """
    北京54坐标系下高斯投影平面坐标(x,y)转大地坐标(BLH)
    
    参数:
    x: float, 北坐标(米)
    y: float, 东坐标(米)
    central_meridian: float, 中央经线(弧度)，如果为None则自动根据投影带计算
    degree_belt: int, 投影带宽，3度带或6度带
    false_easting: float, 东偏移(默认500000米)
    false_northing: float, 北偏移(默认0米)
    
    返回:
    tuple: (B, L, H) 大地纬度(弧度)、大地经度(弧度)、大地高(米)
    """
    # 北京54椭球参数
    a = 6378245.0  # 长半轴
    f = 1/298.3  # 扁率
    e2 = 2*f - f*f  # 第一偏心率平方
    e_prime2 = e2/(1-e2)  # 第二偏心率平方
    
    # 还原坐标（减去偏移量）
    x_f = x - false_northing
    y_f = y - false_easting
    
    # 计算底点纬度的初始值（Bf）
    Mf = x_f  # 子午线弧长
    mu = Mf / (a * (1 - e2/4 - 3*e2**2/64 - 5*e2**3/256))
    
    # 计算底点纬度
    Bf = mu + (3*e2/8 + 3*e2**2/32 + 45*e2**3/1024) * np.sin(2*mu) \
         + (15*e2**2/256 + 45*e2**3/1024) * np.sin(4*mu) \
         + (35*e2**3/3072) * np.sin(6*mu)
    
    # 计算辅助参数
    sin_Bf = np.sin(Bf)
    cos_Bf = np.cos(Bf)
    tan_Bf = np.tan(Bf)
    
    Nf = a / np.sqrt(1 - e2 * sin_Bf**2)  # 卯酉圈曲率半径
    eta2 = e_prime2 * cos_Bf**2
    tf = tan_Bf
    
    # 计算经度偏差
    l = y_f / (Nf * cos_Bf) * (1 - y_f**2/(6 * Nf**2 * cos_Bf**2) * (1 + 2*tf**2 + eta2) \
        + y_f**4/(120 * Nf**4 * cos_Bf**4) * (5 + 28*tf**2 + 24*tf**4 + 6*eta2 + 8*eta2*tf**2))
    
    # 计算纬度偏差
    B = Bf - (y_f**2 * tf / (2 * Nf**2)) * (1 - y_f**2/(12 * Nf**2 * cos_Bf**2) * (5 + 3*tf**2 + eta2 - 9*eta2*tf**2) \
        + y_f**4/(360 * Nf**4 * cos_Bf**4) * (61 + 90*tf**2 + 45*tf**4))
    
    # 计算经度
    if central_meridian is None:
        # 根据投影带宽计算大致中央经线
        if degree_belt == 3:
            # 估计带号
            zone_number = int(y / false_easting + 0.5)
            central_meridian = (zone_number * 3 - 1.5) * np.pi / 180
        else:
            # 估计带号
            zone_number = int(y / false_easting + 0.5)
            central_meridian = (zone_number * 6 - 3) * np.pi / 180
    
    L = central_meridian + l
    
    return B, L