from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, 
                            QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
                            QRadioButton, QHBoxLayout, QLineEdit, QFrame, QSizePolicy,
                            QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy as np
import math
from .seven_param_page import SevenParamPage
from function.WGS84_BLH_XYZ_xy import WGS84_BLH2XYZ, WGS84_XYZ2BLH, WGS84_BLH2xy, WGS84_xy2BLH
from function.Beijing54_BLH_XYZ_xy import Beijing54_BLH2XYZ, Beijing54_XYZ2BLH, Beijing54_BLH2xy, Beijing54_xy2BLH
from function.seven_par import transform_point_seven_par

class TransformPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)  # 增加布局间距
        
        # 应用下拉框通用样式
        combo_style = """
            QComboBox {
                padding: 6px 10px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background: white;
                min-width: 90px;
                font-family: 'Microsoft YaHei UI';
                font-size: 13px;
            }
            
            QComboBox:hover {
                border: 1px solid #BBDEFB;
            }
            
            QComboBox:focus {
                border: 1px solid #2196F3;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: url(resources/down_arrow.png);
                width: 12px;
                height: 12px;
            }
            
            QComboBox QAbstractItemView {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                selection-background-color: #BBDEFB;
                selection-color: #333333;
                background-color: white;
                padding: 4px;
            }
        """
        
        # 设置标签通用样式
        label_style = "QLabel {font-family: 'Microsoft YaHei UI'; font-size: 13px; margin-right: 0px;}"
        
        # 参数选择
        param_group = QGroupBox("转换参数设置")
        param_group.setStyleSheet("QGroupBox {font-weight: bold; font-size: 14px; margin-top: 8px; padding-top: 16px;}")
        param_layout = QGridLayout()
        param_layout.setVerticalSpacing(15)  # 增加垂直间距
        param_layout.setHorizontalSpacing(10)  # 减少水平间距
        
        # 参数类型选择
        param_label = QLabel("转换类型：")
        param_label.setStyleSheet(label_style)
        param_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.param_combo = QComboBox()
        self.param_combo.addItems(["七参数转换","四参数转换"])
        self.param_combo.currentIndexChanged.connect(self.on_param_type_changed)
        self.param_combo.setMinimumHeight(30)
        self.param_combo.setStyleSheet(combo_style)
        param_layout.addWidget(param_label, 0, 0)
        param_layout.addWidget(self.param_combo, 0, 1)
        
        # 源坐标系设置
        source_coord_label = QLabel("源坐标系：")
        source_coord_label.setStyleSheet(label_style)
        source_coord_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.source_coord_combo = QComboBox()
        self.source_coord_combo.addItems(["空间直角坐标系（地心地固坐标系）", "大地坐标（椭球基准下的地理坐标）", "平面坐标（椭球基准下的投影坐标）"])
        self.source_coord_combo.currentIndexChanged.connect(self.on_coord_type_changed)
        self.source_coord_combo.setMinimumHeight(30)
        self.source_coord_combo.setStyleSheet(combo_style)
        
        source_ellipsoid_label = QLabel("源椭球基准：")
        source_ellipsoid_label.setStyleSheet(label_style)
        source_ellipsoid_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.source_ellipsoid_combo = QComboBox()
        self.source_ellipsoid_combo.addItems(["WGS84","北京54"])
        self.source_ellipsoid_combo.setMinimumHeight(30)
        self.source_ellipsoid_combo.setStyleSheet(combo_style)
        
        param_layout.addWidget(source_coord_label, 1, 0)
        param_layout.addWidget(self.source_coord_combo, 1, 1)
        param_layout.addWidget(source_ellipsoid_label, 1, 2)
        param_layout.addWidget(self.source_ellipsoid_combo, 1, 3)
        
        # 目标坐标系设置
        target_coord_label = QLabel("目标坐标系：")
        target_coord_label.setStyleSheet(label_style)
        target_coord_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.target_coord_combo = QComboBox()
        self.target_coord_combo.addItems(["空间直角坐标系（地心地固坐标系）", "大地坐标（椭球基准下的地理坐标）", "平面坐标（椭球基准下的投影坐标）"])
        self.target_coord_combo.currentIndexChanged.connect(self.on_coord_type_changed)
        self.target_coord_combo.setMinimumHeight(30)
        self.target_coord_combo.setStyleSheet(combo_style)
        
        target_ellipsoid_label = QLabel("目标椭球基准：")
        target_ellipsoid_label.setStyleSheet(label_style)
        target_ellipsoid_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.target_ellipsoid_combo = QComboBox()
        self.target_ellipsoid_combo.addItems(["WGS84","北京54"])
        self.target_ellipsoid_combo.setMinimumHeight(30)
        self.target_ellipsoid_combo.setStyleSheet(combo_style)
        
        param_layout.addWidget(target_coord_label, 2, 0)
        param_layout.addWidget(self.target_coord_combo, 2, 1)
        param_layout.addWidget(target_ellipsoid_label, 2, 2)
        param_layout.addWidget(self.target_ellipsoid_combo, 2, 3)
        
        # 大地坐标单位选择框（初始隐藏）
        self.source_unit_frame = QFrame()
        source_unit_layout = QHBoxLayout(self.source_unit_frame)
        source_unit_layout.setContentsMargins(0, 0, 0, 0)
        source_unit_label = QLabel("源坐标单位：")
        source_unit_label.setStyleSheet(label_style)
        self.source_unit_degree = QRadioButton("度")
        self.source_unit_dms = QRadioButton("度分秒")
        self.source_unit_degree.setChecked(True)
        self.source_unit_degree.setStyleSheet("QRadioButton { font-family: 'Microsoft YaHei UI'; }")
        self.source_unit_dms.setStyleSheet("QRadioButton { font-family: 'Microsoft YaHei UI'; }")
        source_unit_layout.addWidget(source_unit_label)
        source_unit_layout.addWidget(self.source_unit_degree)
        source_unit_layout.addWidget(self.source_unit_dms)
        source_unit_layout.addStretch()
        self.source_unit_frame.setVisible(False)
        
        param_layout.addWidget(self.source_unit_frame, 3, 0, 1, 2)
        
        param_group.setLayout(param_layout)
        
        # 定义输入框样式
        input_style = """
            QLineEdit {
                padding: 6px 8px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
                font-family: 'Microsoft YaHei UI';
                font-size: 13px;
            }
            QLineEdit:hover {
                border: 1px solid #BBDEFB;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """
        
        output_style = """
            QLineEdit {
                padding: 6px 8px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background-color: #f8f8f8;
                font-family: 'Microsoft YaHei UI';
                font-size: 13px;
            }
        """
        
        # 投影参数设置
        projection_group = QGroupBox("投影参数设置")
        projection_group.setStyleSheet("QGroupBox {font-weight: bold; font-size: 14px; margin-top: 8px; padding-top: 16px;}")
        projection_layout = QGridLayout()
        projection_layout.setVerticalSpacing(15)
        projection_layout.setHorizontalSpacing(10)
        
        # 投影方式
        projection_type_label = QLabel("投影方式：")
        projection_type_label.setStyleSheet(label_style)
        projection_type_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.projection_type_combo = QComboBox()
        self.projection_type_combo.addItems(["高斯投影3度带", "高斯投影6度带"])
        self.projection_type_combo.setMinimumHeight(30)
        self.projection_type_combo.setStyleSheet(combo_style)
        projection_layout.addWidget(projection_type_label, 0, 0)
        projection_layout.addWidget(self.projection_type_combo, 0, 1)
        
        # 中央子午线
        central_meridian_label = QLabel("中央子午线：")
        central_meridian_label.setStyleSheet(label_style)
        central_meridian_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.central_meridian_input = QLineEdit()
        self.central_meridian_input.setMinimumHeight(30)
        self.central_meridian_input.setStyleSheet(input_style)
        self.central_meridian_input.setText("114:00:00")
        projection_layout.addWidget(central_meridian_label, 0, 2)
        projection_layout.addWidget(self.central_meridian_input, 0, 3)
        
        projection_group.setLayout(projection_layout)
        
        # 单点转换区域 - 改为左中右布局
        point_transform_group = QGroupBox("单点坐标转换")
        point_transform_group.setStyleSheet("QGroupBox {font-weight: bold; font-size: 14px; margin-top: 8px; padding-top: 16px;}")
        point_layout = QHBoxLayout()
        point_layout.setSpacing(20)  # 增加间距
        
        # 左侧 - 源坐标输入
        source_frame = QFrame()
        source_frame.setFrameShape(QFrame.StyledPanel)
        source_frame.setStyleSheet("QFrame {background-color: #f5f5f5; border-radius: 8px;}")
        source_layout = QVBoxLayout(source_frame)
        source_layout.setSpacing(12)
        
        source_title = QLabel("源坐标")
        source_title.setAlignment(Qt.AlignCenter)
        source_title.setFont(QFont("Microsoft YaHei UI", 12, QFont.Bold))
        source_title.setStyleSheet("color: #333; margin-bottom: 8px;")
        source_layout.addWidget(source_title)
        
        # 创建表单布局
        source_grid = QGridLayout()
        source_grid.setHorizontalSpacing(3)  # 标签和输入框之间的间距减小
        source_grid.setVerticalSpacing(12)
        
        # X坐标
        self.source_x_label = QLabel("X:")
        self.source_x_label.setStyleSheet(label_style)
        self.source_x_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.source_x_input = QLineEdit()
        self.source_x_input.setMinimumHeight(30)
        self.source_x_input.setStyleSheet(input_style)
        source_grid.addWidget(self.source_x_label, 0, 0)
        source_grid.addWidget(self.source_x_input, 0, 1)
        
        # Y坐标
        self.source_y_label = QLabel("Y:")
        self.source_y_label.setStyleSheet(label_style)
        self.source_y_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.source_y_input = QLineEdit()
        self.source_y_input.setMinimumHeight(30)
        self.source_y_input.setStyleSheet(input_style)
        source_grid.addWidget(self.source_y_label, 1, 0)
        source_grid.addWidget(self.source_y_input, 1, 1)
        
        # Z坐标
        self.source_z_label = QLabel("Z:")
        self.source_z_label.setStyleSheet(label_style)
        self.source_z_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.source_z_input = QLineEdit()
        self.source_z_input.setMinimumHeight(30)
        self.source_z_input.setStyleSheet(input_style)
        source_grid.addWidget(self.source_z_label, 2, 0)
        source_grid.addWidget(self.source_z_input, 2, 1)
        
        source_layout.addLayout(source_grid)
        source_layout.addStretch(1)
        
        # 中间 - 转换按钮
        center_frame = QFrame()
        center_layout = QVBoxLayout(center_frame)
        center_layout.setAlignment(Qt.AlignCenter)
        
        transform_btn = QPushButton("转换")
        transform_btn.setMinimumSize(100, 40)
        transform_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3; 
                color: white; 
                font-weight: bold;
                font-family: 'Microsoft YaHei UI';
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        transform_btn.clicked.connect(self.transform_coordinates)  # 连接点击事件
        center_layout.addWidget(transform_btn)
        
        # 右侧 - 目标坐标输出
        target_frame = QFrame()
        target_frame.setFrameShape(QFrame.StyledPanel)
        target_frame.setStyleSheet("QFrame {background-color: #e8f5e9; border-radius: 8px;}")
        target_layout = QVBoxLayout(target_frame)
        target_layout.setSpacing(12)
        
        target_title = QLabel("目标坐标")
        target_title.setAlignment(Qt.AlignCenter)
        target_title.setFont(QFont("Microsoft YaHei UI", 12, QFont.Bold))
        target_title.setStyleSheet("color: #333; margin-bottom: 8px;")
        target_layout.addWidget(target_title)
        
        # 创建表单布局
        target_grid = QGridLayout()
        target_grid.setHorizontalSpacing(3)  # 标签和输入框之间的间距减小
        target_grid.setVerticalSpacing(12)
        
        # X坐标
        self.target_x_label = QLabel("X:")
        self.target_x_label.setStyleSheet(label_style)
        self.target_x_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.target_x_output = QLineEdit()
        self.target_x_output.setReadOnly(True)
        self.target_x_output.setMinimumHeight(30)
        self.target_x_output.setStyleSheet(output_style)
        target_grid.addWidget(self.target_x_label, 0, 0)
        target_grid.addWidget(self.target_x_output, 0, 1)
        
        # Y坐标
        self.target_y_label = QLabel("Y:")
        self.target_y_label.setStyleSheet(label_style)
        self.target_y_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.target_y_output = QLineEdit()
        self.target_y_output.setReadOnly(True)
        self.target_y_output.setMinimumHeight(30)
        self.target_y_output.setStyleSheet(output_style)
        target_grid.addWidget(self.target_y_label, 1, 0)
        target_grid.addWidget(self.target_y_output, 1, 1)
        
        # Z坐标
        self.target_z_label = QLabel("Z:")
        self.target_z_label.setStyleSheet(label_style)
        self.target_z_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.target_z_output = QLineEdit()
        self.target_z_output.setReadOnly(True)
        self.target_z_output.setMinimumHeight(30)
        self.target_z_output.setStyleSheet(output_style)
        target_grid.addWidget(self.target_z_label, 2, 0)
        target_grid.addWidget(self.target_z_output, 2, 1)
        
        target_layout.addLayout(target_grid)
        target_layout.addStretch(1)
        
        # 添加三个面板到左中右布局
        point_layout.addWidget(source_frame, 3)
        point_layout.addWidget(center_frame, 1)
        point_layout.addWidget(target_frame, 3)
        
        point_transform_group.setLayout(point_layout)
        
        # 添加到主布局
        layout.addWidget(param_group)
        layout.addWidget(projection_group)
        layout.addWidget(point_transform_group)
        
        # 设置初始坐标标签
        self.update_coordinate_labels("空间直角坐标系", "空间直角坐标系")
    
    def on_param_type_changed(self, index):
        param_type = self.param_combo.currentText()
        
        # 七参数转换需要选择源和目标椭球基准
        if param_type == "七参数转换":
            self.source_ellipsoid_combo.setEnabled(True)
            self.target_ellipsoid_combo.setEnabled(True)
            
            # 启用所有坐标类型选择
            self.source_coord_combo.clear()
            self.source_coord_combo.addItems(["空间直角坐标系（地心地固坐标系）", "大地坐标（椭球基准下的地理坐标）", "平面坐标（椭球基准下的投影坐标）"])
            self.target_coord_combo.clear()
            self.target_coord_combo.addItems(["空间直角坐标系（地心地固坐标系）", "大地坐标（椭球基准下的地理坐标）", "平面坐标（椭球基准下的投影坐标）"])
        
        # 四参数转换只能使用平面坐标，只需要选择一个椭球基准
        elif param_type == "四参数转换":
            self.source_ellipsoid_combo.setEnabled(True)
            self.target_ellipsoid_combo.setEnabled(False)
            
            # 限制只能选择平面坐标
            self.source_coord_combo.clear()
            self.source_coord_combo.addItems(["平面坐标（椭球基准下的投影坐标）"])
            self.target_coord_combo.clear()
            self.target_coord_combo.addItems(["平面坐标（椭球基准下的投影坐标）"])
            
            # 更新坐标标签
            self.update_coordinate_labels("平面坐标", "平面坐标")
    
    def on_coord_type_changed(self, index):
        source_type = self.source_coord_combo.currentText()
        target_type = self.target_coord_combo.currentText()
        
        # 更新坐标标签
        self.update_coordinate_labels(source_type, target_type)
        
        # 显示/隐藏大地坐标单位选择 - 使用关键词索引而不是完全匹配
        self.source_unit_frame.setVisible("大地坐标" in source_type)
    
    def update_coordinate_labels(self, source_type, target_type):
        # 使用关键词索引来更新坐标标签
        # 更新源坐标标签
        if "空间直角" in source_type:
            self.source_x_label.setText("X:")
            self.source_y_label.setText("Y:")
            self.source_z_label.setText("Z:")
        elif "大地坐标" in source_type:
            self.source_x_label.setText("B:")
            self.source_y_label.setText("L:")
            self.source_z_label.setText("H:")
        elif "平面坐标" in source_type:
            self.source_x_label.setText("x:")
            self.source_y_label.setText("y:")
            self.source_z_label.setText("h:")
        
        # 更新目标坐标标签
        if "空间直角" in target_type:
            self.target_x_label.setText("X:")
            self.target_y_label.setText("Y:")
            self.target_z_label.setText("Z:")
        elif "大地坐标" in target_type:
            self.target_x_label.setText("B:")
            self.target_y_label.setText("L:")
            self.target_z_label.setText("H:")
        elif "平面坐标" in target_type:
            self.target_x_label.setText("x:")
            self.target_y_label.setText("y:")
            self.target_z_label.setText("h:") 
    
    def transform_coordinates(self):
        """坐标转换计算函数"""
        try:
            # 获取转换类型
            transform_type = self.param_combo.currentText()
            source_coord_type = self.source_coord_combo.currentText()
            target_coord_type = self.target_coord_combo.currentText()
            
            # 获取输入坐标值
            # 如果是大地坐标且选择了度分秒格式，需要特殊处理
            if "大地坐标" in source_coord_type and self.source_unit_dms.isChecked():
                try:
                    x_text = self.source_x_input.text() or "0:0:0"
                    y_text = self.source_y_input.text() or "0:0:0"
                    
                    # 解析度分秒格式
                    x = self.parse_dms_to_decimal(x_text)  # B
                    y = self.parse_dms_to_decimal(y_text)  # L
                    z = float(self.source_z_input.text() or 0)  # H
                except ValueError as e:
                    raise ValueError(f"度分秒格式错误: {str(e)}")
            else:
                # 其他坐标格式，直接解析为浮点数
                x = float(self.source_x_input.text() or 0)
                y = float(self.source_y_input.text() or 0)
                z = float(self.source_z_input.text() or 0)
            
            if transform_type == "七参数转换":
                # 获取椭球基准
                source_ellipsoid = self.source_ellipsoid_combo.currentText()
                target_ellipsoid = self.target_ellipsoid_combo.currentText()
                
                # 获取七参数页面的计算结果
                # 从主窗口查找七参数页面
                main_window = self.window()
                tab_widget = main_window.findChild(QTabWidget)
                seven_param_page = None
                
                if tab_widget:
                    # 查找七参数页面
                    for i in range(tab_widget.count()):
                        if "七参数" in tab_widget.tabText(i):
                            seven_param_page = tab_widget.widget(i)
                            break
                
                # 如果找不到七参数页面，显示错误信息
                if not seven_param_page:
                    QMessageBox.warning(self, "参数错误", "无法获取七参数页面，请确保七参数页面已创建")
                    return
                
                # 获取七参数值
                try:
                    # 使用与main_window.py相同的方式获取参数
                    dx = float(seven_param_page.findChild(QLineEdit, 'dx_result').text().split()[0]) if seven_param_page.findChild(QLineEdit, 'dx_result') and seven_param_page.findChild(QLineEdit, 'dx_result').text() else None
                    dy = float(seven_param_page.findChild(QLineEdit, 'dy_result').text().split()[0]) if seven_param_page.findChild(QLineEdit, 'dy_result') and seven_param_page.findChild(QLineEdit, 'dy_result').text() else None
                    dz = float(seven_param_page.findChild(QLineEdit, 'dz_result').text().split()[0]) if seven_param_page.findChild(QLineEdit, 'dz_result') and seven_param_page.findChild(QLineEdit, 'dz_result').text() else None
                    wx = float(seven_param_page.findChild(QLineEdit, 'wx_result').text().split()[0]) if seven_param_page.findChild(QLineEdit, 'wx_result') and seven_param_page.findChild(QLineEdit, 'wx_result').text() else None
                    wy = float(seven_param_page.findChild(QLineEdit, 'wy_result').text().split()[0]) if seven_param_page.findChild(QLineEdit, 'wy_result') and seven_param_page.findChild(QLineEdit, 'wy_result').text() else None
                    wz = float(seven_param_page.findChild(QLineEdit, 'wz_result').text().split()[0]) if seven_param_page.findChild(QLineEdit, 'wz_result') and seven_param_page.findChild(QLineEdit, 'wz_result').text() else None
                    k = float(seven_param_page.findChild(QLineEdit, 'k_result').text().split()[0]) if seven_param_page.findChild(QLineEdit, 'k_result') and seven_param_page.findChild(QLineEdit, 'k_result').text() else None
                    
                    # 检查是否有任何参数为None
                    if None in [dx, dy, dz, wx, wy, wz, k]:
                        QMessageBox.warning(self, "参数错误", "七参数不完整，请先在七参数页面计算七参数")
                        return
                    
                    # 创建参数数组
                    parameters = np.array([dx, dy, dz, wx, wy, wz, k])
                    
                except (AttributeError, ValueError, IndexError) as e:
                    # 如果参数获取失败
                    QMessageBox.warning(self, "参数错误", f"无法获取七参数: {str(e)}\n请先在七参数页面计算七参数")
                    return
                
                print(f"【坐标转换】使用七参数: {parameters}")
                
                # 不同坐标系的转换逻辑
                if "空间直角" in source_coord_type and "空间直角" in target_coord_type:
                    # 空间直角坐标系到空间直角坐标系的七参数转换
                    xyz = transform_point_seven_par(
                        np.array([x, y, z]), parameters
                    )
                    result_x, result_y, result_z = xyz[0], xyz[1], xyz[2]
                    
                elif "空间直角" in source_coord_type:
                    # 先进行七参数转换得到目标椭球下的空间直角坐标
                    xyz = transform_point_seven_par(
                        np.array([x, y, z]), parameters
                    )
                    
                    # 然后根据目标坐标类型进行转换
                    if "大地坐标" in target_coord_type:
                        # 空间直角坐标转大地坐标
                        if target_ellipsoid == "WGS84":
                            b, l, h = WGS84_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        else:  # 北京54
                            b, l, h = Beijing54_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        
                        # 弧度转换为度
                        result_x, result_y, result_z = np.degrees(b), np.degrees(l), h
                        
                    elif "平面坐标" in target_coord_type:
                        # 空间直角坐标转大地坐标
                        if target_ellipsoid == "WGS84":
                            b, l, h = WGS84_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        else:  # 北京54
                            b, l, h = Beijing54_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        
                        # 然后转平面坐标
                        central_meridian = self.get_central_meridian()
                        if target_ellipsoid == "WGS84":
                            y, x = WGS84_BLH2xy(b, l, central_meridian)
                            result_x, result_y, result_z = x, y, h
                        else:  # 北京54
                            y, x = Beijing54_BLH2xy(b, l, central_meridian)
                            result_x, result_y, result_z = x, y, h
                
                elif "大地坐标" in source_coord_type:
                    # 先将大地坐标转为空间直角坐标
                    # 如果已经在上面解析为十进制度，这里不需要再次转换
                    if self.source_unit_dms.isChecked():
                        # 已在上面解析为十进制度，这里转为弧度
                        b_rad = np.radians(x)
                        l_rad = np.radians(y)
                    else:
                        # 度转弧度
                        b_rad = np.radians(x) if self.source_unit_degree.isChecked() else x
                        l_rad = np.radians(y) if self.source_unit_degree.isChecked() else y
                    h = z
                    
                    # 转换为空间直角坐标
                    if source_ellipsoid == "WGS84":
                        x_xyz, y_xyz, z_xyz = WGS84_BLH2XYZ(b_rad, l_rad, h)
                    else:  # 北京54
                        x_xyz, y_xyz, z_xyz = Beijing54_BLH2XYZ(b_rad, l_rad, h)
                    
                    # 进行七参数转换
                    xyz = transform_point_seven_par(
                        np.array([x_xyz, y_xyz, z_xyz]), parameters
                    )
                    
                    # 根据目标坐标类型进行转换
                    if "空间直角" in target_coord_type:
                        result_x, result_y, result_z = xyz[0], xyz[1], xyz[2]
                    elif "大地坐标" in target_coord_type:
                        # 转换为大地坐标
                        if target_ellipsoid == "WGS84":
                            b, l, h = WGS84_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        else:  # 北京54
                            b, l, h = Beijing54_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        
                        # 弧度转换为度
                        result_x, result_y, result_z = np.degrees(b), np.degrees(l), h
                            
                    elif "平面坐标" in target_coord_type:
                        # 转换为大地坐标
                        if target_ellipsoid == "WGS84":
                            b, l, h = WGS84_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        else:  # 北京54
                            b, l, h = Beijing54_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        
                        # 然后转平面坐标
                        central_meridian = self.get_central_meridian()
                        if target_ellipsoid == "WGS84":
                            y, x = WGS84_BLH2xy(b, l, central_meridian)
                            result_x, result_y, result_z = x, y, h
                        else:  # 北京54
                            y, x = Beijing54_BLH2xy(b, l, central_meridian)
                            result_x, result_y, result_z = x, y, h
                
                elif "平面坐标" in source_coord_type:
                    # 获取中央子午线
                    central_meridian = self.get_central_meridian()
                    
                    # 平面坐标转大地坐标
                    if source_ellipsoid == "WGS84":
                        b, l = WGS84_xy2BLH(x, y, central_meridian)
                        h = z
                    else:  # 北京54
                        b, l = Beijing54_xy2BLH(x, y, central_meridian)
                        h = z
                    
                    # 大地坐标转空间直角坐标
                    if source_ellipsoid == "WGS84":
                        x_xyz, y_xyz, z_xyz = WGS84_BLH2XYZ(b, l, h)
                    else:  # 北京54
                        x_xyz, y_xyz, z_xyz = Beijing54_BLH2XYZ(b, l, h)
                    
                    # 七参数转换
                    xyz = transform_point_seven_par(
                        np.array([x_xyz, y_xyz, z_xyz]), parameters
                    )
                    
                    # 转换为目标坐标系
                    if "空间直角" in target_coord_type:
                        result_x, result_y, result_z = xyz[0], xyz[1], xyz[2]
                    elif "大地坐标" in target_coord_type:
                        # 转换为大地坐标
                        if target_ellipsoid == "WGS84":
                            b, l, h = WGS84_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        else:  # 北京54
                            b, l, h = Beijing54_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        
                        # 弧度转换为度
                        result_x, result_y, result_z = np.degrees(b), np.degrees(l), h
                            
                    elif "平面坐标" in target_coord_type:
                        # 转换为大地坐标
                        if target_ellipsoid == "WGS84":
                            b, l, h = WGS84_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        else:  # 北京54
                            b, l, h = Beijing54_XYZ2BLH(xyz[0], xyz[1], xyz[2])
                        
                        # 然后转平面坐标
                        if target_ellipsoid == "WGS84":
                            y, x = WGS84_BLH2xy(b, l, central_meridian)
                            result_x, result_y, result_z = x, y, h
                        else:  # 北京54
                            y, x = Beijing54_BLH2xy(b, l, central_meridian)
                            result_x, result_y, result_z = x, y, h
                
                # 显示结果
                self.target_x_output.setText(f"{result_x:.8f}")
                self.target_y_output.setText(f"{result_y:.8f}")
                self.target_z_output.setText(f"{result_z:.8f}")
            
            elif transform_type == "四参数转换":
                # 四参数转换逻辑
                # 从主窗口查找四参数页面
                main_window = self.window()
                tab_widget = main_window.findChild(QTabWidget)
                four_param_page = None
                
                if tab_widget:
                    # 查找四参数页面
                    for i in range(tab_widget.count()):
                        if "四参数" in tab_widget.tabText(i):
                            four_param_page = tab_widget.widget(i)
                            break
                
                # 如果找不到四参数页面，显示错误信息
                if not four_param_page:
                    QMessageBox.warning(self, "参数错误", "无法获取四参数页面，请确保四参数页面已创建")
                    return
                
                # 获取四参数值
                try:
                    # 使用与七参数页面相同的方式获取参数
                    a = float(four_param_page.findChild(QLineEdit, 'a_result').text().split()[0]) if four_param_page.findChild(QLineEdit, 'a_result') and four_param_page.findChild(QLineEdit, 'a_result').text() else None
                    b = float(four_param_page.findChild(QLineEdit, 'b_result').text().split()[0]) if four_param_page.findChild(QLineEdit, 'b_result') and four_param_page.findChild(QLineEdit, 'b_result').text() else None
                    dx = float(four_param_page.findChild(QLineEdit, 'dx_result').text().split()[0]) if four_param_page.findChild(QLineEdit, 'dx_result') and four_param_page.findChild(QLineEdit, 'dx_result').text() else None
                    dy = float(four_param_page.findChild(QLineEdit, 'dy_result').text().split()[0]) if four_param_page.findChild(QLineEdit, 'dy_result') and four_param_page.findChild(QLineEdit, 'dy_result').text() else None
                    
                    # 检查是否有任何参数为None
                    if None in [a, b, dx, dy]:
                        QMessageBox.warning(self, "参数错误", "四参数不完整，请先在四参数页面计算四参数")
                        return
                    
                    # 创建参数数组
                    parameters = {'a': a, 'b': b, 'dx': dx, 'dy': dy}
                    
                except (AttributeError, ValueError, IndexError) as e:
                    # 如果参数获取失败
                    QMessageBox.warning(self, "参数错误", f"无法获取四参数: {str(e)}\n请先在四参数页面计算四参数")
                    return
                
                print(f"【坐标转换】使用四参数: {parameters}")
                
                # 调用四参数转换函数
                from function.four_par import transform_point_four_par
                
                # 由于四参数只能用于平面坐标系转换，所以直接使用输入的x和y值
                transformed_point = transform_point_four_par((x, y), parameters)
                result_x, result_y = transformed_point
                result_z = z  # 高度值通常不变
                
                # 显示结果
                self.target_x_output.setText(f"{result_x:.8f}")
                self.target_y_output.setText(f"{result_y:.8f}")
                self.target_z_output.setText(f"{result_z:.8f}")
        
        except ValueError as e:
            QMessageBox.warning(self, "输入错误", f"请输入有效的数字: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"计算过程中发生错误: {str(e)}")
    
    def get_central_meridian(self):
        """获取中央子午线，默认为120度"""
        central_meridian_text = self.central_meridian_input.text().strip()
        if not central_meridian_text:
            return np.radians(120.0)  # 默认值
        
        # 移除度符号
        central_meridian_text = central_meridian_text.replace('°', '')
        
        try:
            # 检查是否为度分秒格式 (dd:mm:ss.s)
            if ':' in central_meridian_text:
                parts = central_meridian_text.split(':')
                if len(parts) != 3:
                    raise ValueError("度分秒格式应为 'dd:mm:ss.s'")
                
                degrees = float(parts[0])
                minutes = float(parts[1])
                seconds = float(parts[2])
                
                # 检查分和秒是否在有效范围内
                if minutes >= 60 or seconds >= 60:
                    raise ValueError("分和秒必须小于60")
                
                # 计算十进制度
                sign = -1 if degrees < 0 else 1
                decimal_degrees = abs(degrees) + minutes/60 + seconds/3600
                decimal_degrees = sign * decimal_degrees
                
                return np.radians(decimal_degrees)
            else:
                # 直接解析为浮点数
                central_meridian = float(central_meridian_text)
                return np.radians(central_meridian)
        except ValueError as e:
            raise ValueError(f"无法解析中央子午线值: {central_meridian_text} - {str(e)}")
    
    def parse_dms_to_decimal(self, dms_str):
        """将度分秒格式转换为十进制度"""
        # 移除可能的空格和度符号
        dms_str = dms_str.strip().replace('°', '')
        
        try:
            # 检查是否为度分秒格式 (dd:mm:ss.s)
            if ':' in dms_str:
                parts = dms_str.split(':')
                if len(parts) != 3:
                    raise ValueError("度分秒格式应为 'dd:mm:ss.s'")
                
                degrees = float(parts[0])
                minutes = float(parts[1])
                seconds = float(parts[2])
                
                # 检查分和秒是否在有效范围内
                if minutes >= 60 or seconds >= 60:
                    raise ValueError("分和秒必须小于60")
                
                # 计算十进制度
                sign = -1 if degrees < 0 else 1
                decimal_degrees = abs(degrees) + minutes/60 + seconds/3600
                decimal_degrees = sign * decimal_degrees
                
                return decimal_degrees
            else:
                # 直接解析为浮点数
                return float(dms_str)
        except ValueError as e:
            raise ValueError(f"无法解析度分秒值: {dms_str} - {str(e)}") 