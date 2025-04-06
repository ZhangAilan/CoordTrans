from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                           QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                           QRadioButton, QComboBox, QLineEdit, QGroupBox, QMessageBox,
                           QCheckBox)
from PyQt5.QtCore import Qt
import re
import numpy as np
from function.WGS84_BLH_XYZ_xy import WGS84_BLH2XYZ, WGS84_XYZ2BLH
from function.Beijing54_BLH_XYZ_xy import Beijing54_BLH2XYZ, Beijing54_XYZ2BLH
from function.seven_par import bursa_seven_parameters

class SevenParamPage(QWidget):
    def __init__(self):
        super().__init__()
        self.editing_row = None  # 添加编辑行的标记
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 创建上部分布局
        top_layout = QHBoxLayout()
        
        # 源坐标系组
        source_group = QGroupBox("输入源坐标")
        source_layout = QGridLayout()
        
        # 添加源坐标系控件
        coord_type_layout1 = QHBoxLayout()
        self.unit_combo1 = QComboBox()
        self.unit_combo1.addItems(["度:分:秒", "度"])
        self.blh_radio1 = QRadioButton("大地坐标BLH")
        self.blh_radio1.setChecked(True)
        self.xyz_radio1 = QRadioButton("空间直角坐标XYH")
        
        coord_type_layout1.addWidget(self.unit_combo1)
        coord_type_layout1.addWidget(self.blh_radio1)
        coord_type_layout1.addWidget(self.xyz_radio1)
        
        self.b_label = QLabel("B=")
        self.l_label = QLabel("L=")
        self.h_label = QLabel("H=")
        
        self.b_input = QLineEdit()
        self.l_input = QLineEdit()
        self.h_input = QLineEdit()
        
        self.coord_system1 = QComboBox()
        self.coord_system1.addItem("WGS-84坐标系")
        self.coord_system1.addItem("北京54坐标系")
        
        # 连接源坐标系单选按钮信号
        self.blh_radio1.toggled.connect(self.on_source_radio_toggled)
        self.blh_radio1.toggled.connect(lambda checked: self.unit_combo1.setVisible(checked))
        
        # 布局源坐标系控件
        source_layout.addLayout(coord_type_layout1, 0, 0, 1, 2)
        source_layout.addWidget(self.b_label, 1, 0)
        source_layout.addWidget(self.b_input, 1, 1)
        source_layout.addWidget(self.l_label, 2, 0)
        source_layout.addWidget(self.l_input, 2, 1)
        source_layout.addWidget(self.h_label, 3, 0)
        source_layout.addWidget(self.h_input, 3, 1)
        source_layout.addWidget(QLabel("椭球基准:"), 4, 0)
        source_layout.addWidget(self.coord_system1, 4, 1)
        
        source_group.setLayout(source_layout)
        
        # 目标坐标系组
        target_group = QGroupBox("输入目标坐标")
        target_layout = QGridLayout()
        
        # 添加目标坐标系控件
        coord_type_layout2 = QHBoxLayout()
        self.unit_combo2 = QComboBox()
        self.unit_combo2.addItems(["度:分:秒", "度"])
        self.blh_radio2 = QRadioButton("大地坐标BLH")
        self.blh_radio2.setChecked(True)
        self.xyz_radio2 = QRadioButton("空间直角坐标XYH")
        
        coord_type_layout2.addWidget(self.unit_combo2)
        coord_type_layout2.addWidget(self.blh_radio2)
        coord_type_layout2.addWidget(self.xyz_radio2)
        
        self.x_label = QLabel("B=")
        self.y_label = QLabel("L=")
        self.h2_label = QLabel("H=")
        
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.h2_input = QLineEdit()
        
        self.coord_system2 = QComboBox()
        self.coord_system2.addItem("北京54坐标系")
        self.coord_system2.addItem("WGS-84坐标系")
        
        # 连接目标坐标系单选按钮信号
        self.blh_radio2.toggled.connect(self.on_target_radio_toggled)
        self.blh_radio2.toggled.connect(lambda checked: self.unit_combo2.setVisible(checked))
        
        # 布局目标坐标系控件
        target_layout.addLayout(coord_type_layout2, 0, 0, 1, 2)
        target_layout.addWidget(self.x_label, 1, 0)
        target_layout.addWidget(self.x_input, 1, 1)
        target_layout.addWidget(self.y_label, 2, 0)
        target_layout.addWidget(self.y_input, 2, 1)
        target_layout.addWidget(self.h2_label, 3, 0)
        target_layout.addWidget(self.h2_input, 3, 1)
        target_layout.addWidget(QLabel("椭球基准:"), 4, 0)
        target_layout.addWidget(self.coord_system2, 4, 1)
        
        target_group.setLayout(target_layout)
        
        # 修改计算结果组
        result_group = QGroupBox("计算结果")
        result_layout = QGridLayout()
        
        # 添加七参数结果显示
        params = [
            ("DX:", "dx_result"), ("DY:", "dy_result"), ("DZ:", "dz_result"),
            ("WX:", "wx_result"), ("WY:", "wy_result"), ("WZ:", "wz_result"),
            ("K:", "k_result")
        ]
        
        for row, (label_text, name) in enumerate(params):
            label = QLabel(label_text)
            result = QLineEdit()
            result.setReadOnly(True)
            result.setObjectName(name)
            result_layout.addWidget(label, row, 0)
            result_layout.addWidget(result, row, 1)
        
        result_group.setLayout(result_layout)
        
        # 将三个组添加到顶部布局
        top_layout.addWidget(source_group)
        top_layout.addWidget(target_group)
        top_layout.addWidget(result_group)
        
        # 修改按钮工具栏
        button_layout = QHBoxLayout()
        buttons = ["增加", "编辑", "删除", "计算"]
        for text in buttons:
            btn = QPushButton(text)
            if text == "增加":
                btn.clicked.connect(self.on_add_clicked)
            elif text == "编辑":
                btn.clicked.connect(self.on_edit_clicked)
            elif text == "删除":
                btn.clicked.connect(self.on_delete_clicked)
            elif text == "计算":
                btn.clicked.connect(self.on_calculate_clicked)
            button_layout.addWidget(btn)
        
        # 创建数据表格
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        headers = ["选择", "源坐标B/X", "源坐标L/Y", "源坐标H/Z", 
                  "目标坐标B/X", "目标坐标L/Y", "目标坐标H/Z", "RMS"]
        self.table.setHorizontalHeaderLabels(headers)
        
        # 设置表头点击信号连接
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        
        # 调整布局比例
        layout.addLayout(top_layout, stretch=4)
        layout.addLayout(button_layout, stretch=1)
        layout.addWidget(self.table, stretch=5)
        
        # 设置样式
        self.setup_style()
        
    def setup_style(self):
        style = """
            QGroupBox {
                font-family: 'Microsoft YaHei UI';
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 12px;
                padding: 15px;
                padding-top: 25px;
                background-color: #FFFFFF;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 8px;
                color: #333333;
                background-color: #FFFFFF;
            }
            
            QRadioButton {
                font-family: 'Microsoft YaHei UI';
                font-size: 13px;
                color: #333333;
                spacing: 5px;
                padding: 4px;
            }
            
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            
            QRadioButton::indicator:unchecked {
                border: 2px solid #BDBDBD;
                border-radius: 8px;
                background-color: #FFFFFF;
            }
            
            QRadioButton::indicator:checked {
                border: 2px solid #2196F3;
                border-radius: 8px;
                background-color: #346D95;
            }
            
            QLineEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background: white;
                min-width: 120px;
                font-size: 13px;
            }
            
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
            
            QComboBox {
                padding: 6px 10px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background: white;
                min-width: 90px;
                max-width: 110px;
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
            
            QLabel {
                font-family: 'Microsoft YaHei UI';
                font-size: 13px;
                color: #333333;
                padding: 4px;
            }
            
            QPushButton {
                min-width: 80px;
            }
        """
        self.setStyleSheet(style)

    def on_source_radio_toggled(self, checked):
        if checked:  # BLH被选中
            self.b_label.setText("B=")
            self.l_label.setText("L=")
            self.h_label.setText("H=")
        else:  # XYZ被选中
            self.b_label.setText("X=")
            self.l_label.setText("Y=")
            self.h_label.setText("H=")
            
    def on_target_radio_toggled(self, checked):
        if checked:  # BLH被选中
            self.x_label.setText("B=")
            self.y_label.setText("L=")
            self.h2_label.setText("H=")
        else:  # XYZ被选中
            self.x_label.setText("X=")
            self.y_label.setText("Y=")
            self.h2_label.setText("H=") 

    def validate_degree_format(self, value, format_type):
        """验证度数格式"""
        if format_type == "度:分:秒":
            # 验证度分秒格式 (dd:mm:ss.ss)
            pattern = r'^\d{1,3}:\d{1,2}:\d{1,2}(\.\d+)?$'
            if not re.match(pattern, value):
                return False
                
            # 检查分和秒是否在有效范围内
            try:
                deg, min, sec = value.split(':')
                if int(min) >= 60 or float(sec) >= 60:
                    return False
            except:
                return False
                
        else:  # 度格式
            try:
                value = float(value)
                if value < -180 or value > 180:
                    return False
            except:
                return False
                
        return True
        
    def validate_xyz_format(self, value):
        """验证XYZ坐标格式"""
        try:
            value = float(value)
            return True
        except:
            return False
            
    def on_add_clicked(self):
        """处理增加按钮点击事件"""
        # 获取所有输入值
        source_values = [self.b_input.text().strip(), 
                        self.l_input.text().strip(),
                        self.h_input.text().strip()]
        target_values = [self.x_input.text().strip(),
                        self.y_input.text().strip(),
                        self.h2_input.text().strip()]
        
        # 检查是否有空值
        if any(not v for v in source_values + target_values):
            QMessageBox.warning(self, "输入错误", "所有字段都必须填写！")
            return
            
        # 根据单选按钮状态判断输入类型
        source_is_blh = self.blh_radio1.isChecked()
        target_is_blh = self.blh_radio2.isChecked()
        
        # 验证源坐标格式
        if source_is_blh:
            unit_format = self.unit_combo1.currentText()
            if not all(self.validate_degree_format(v, unit_format) 
                      for v in source_values[:2]):
                QMessageBox.warning(self, "输入错误", 
                    f"源坐标B、L必须是有效的{unit_format}格式！")
                return
            if not self.validate_xyz_format(source_values[2]):  # H值验证
                QMessageBox.warning(self, "输入错误", "高程H必须是有效的数值！")
                return
        else:
            if not all(self.validate_xyz_format(v) for v in source_values):
                QMessageBox.warning(self, "输入错误", "XYZ坐标必须是有效的数值！")
                return
                
        # 验证目标坐标格式
        if target_is_blh:
            unit_format = self.unit_combo2.currentText()
            if not all(self.validate_degree_format(v, unit_format) 
                      for v in target_values[:2]):
                QMessageBox.warning(self, "输入错误", 
                    f"目标坐标B、L必须是有效的{unit_format}格式！")
                return
            if not self.validate_xyz_format(target_values[2]):  # H值验证
                QMessageBox.warning(self, "输入错误", "高程H必须是有效的数值！")
                return
        else:
            if not all(self.validate_xyz_format(v) for v in target_values):
                QMessageBox.warning(self, "输入错误", "XYZ坐标必须是有效的数值！")
                return
        
        # 添加到表格
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # 添加复选框
        checkbox = QCheckBox()
        # 连接复选框状态变化信号到更新全选状态的函数
        checkbox.stateChanged.connect(self.update_select_all_state)
        self.table.setCellWidget(row, 0, checkbox)
        
        # 添加坐标值
        for col, value in enumerate(source_values + target_values, 1):
            item = QTableWidgetItem(value)
            self.table.setItem(row, col, item)
            
        # 清空输入框
        self.clear_inputs()
        
    def on_edit_clicked(self):
        """处理编辑按钮点击事件"""
        # 获取选中的行
        selected_rows = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)
        
        # 检查选中的行数
        if len(selected_rows) == 0:
            QMessageBox.warning(self, "提示", "请选择要编辑的行！")
            return
        elif len(selected_rows) > 1:
            QMessageBox.warning(self, "提示", "一次只能编辑一行数据！")
            return
            
        row = selected_rows[0]
        self.editing_row = row
        
        # 将表格数据加载到输入框
        source_values = [self.table.item(row, i).text() for i in range(1, 4)]
        target_values = [self.table.item(row, i).text() for i in range(4, 7)]
        
        # 设置源坐标值
        self.b_input.setText(source_values[0])
        self.l_input.setText(source_values[1])
        self.h_input.setText(source_values[2])
        
        # 设置目标坐标值
        self.x_input.setText(target_values[0])
        self.y_input.setText(target_values[1])
        self.h2_input.setText(target_values[2])
        
        # 修改增加按钮文本为"保存"
        for btn in self.findChildren(QPushButton):
            if btn.text() == "增加":
                btn.setText("保存")
                btn.clicked.disconnect()
                btn.clicked.connect(self.on_save_clicked)
                
    def on_save_clicked(self):
        """处理保存按钮点击事件"""
        if self.editing_row is None:
            return
            
        # 保存当前编辑的行号
        current_row = self.editing_row
            
        # 获取所有输入值并验证（复用增加功能的验证逻辑）
        source_values = [self.b_input.text().strip(), 
                        self.l_input.text().strip(),
                        self.h_input.text().strip()]
        target_values = [self.x_input.text().strip(),
                        self.y_input.text().strip(),
                        self.h2_input.text().strip()]
        
        # 检查是否有空值
        if any(not v for v in source_values + target_values):
            QMessageBox.warning(self, "输入错误", "所有字段都必须填写！")
            return
            
        # 验证格式（复用之前的验证逻辑）
        source_is_blh = self.blh_radio1.isChecked()
        target_is_blh = self.blh_radio2.isChecked()
        
        # 验证源坐标格式
        if source_is_blh:
            unit_format = self.unit_combo1.currentText()
            if not all(self.validate_degree_format(v, unit_format) 
                      for v in source_values[:2]):
                QMessageBox.warning(self, "输入错误", 
                    f"源坐标B、L必须是有效的{unit_format}格式！")
                return
            if not self.validate_xyz_format(source_values[2]):
                QMessageBox.warning(self, "输入错误", "高程H必须是有效的数值！")
                return
        else:
            if not all(self.validate_xyz_format(v) for v in source_values):
                QMessageBox.warning(self, "输入错误", "XYZ坐标必须是有效的数值！")
                return
                
        # 验证目标坐标格式
        if target_is_blh:
            unit_format = self.unit_combo2.currentText()
            if not all(self.validate_degree_format(v, unit_format) 
                      for v in target_values[:2]):
                QMessageBox.warning(self, "输入错误", 
                    f"目标坐标B、L必须是有效的{unit_format}格式！")
                return
            if not self.validate_xyz_format(target_values[2]):
                QMessageBox.warning(self, "输入错误", "高程H必须是有效的数值！")
                return
        else:
            if not all(self.validate_xyz_format(v) for v in target_values):
                QMessageBox.warning(self, "输入错误", "XYZ坐标必须是有效的数值！")
                return
        
        # 更新表格数据
        for col, value in enumerate(source_values + target_values, 1):
            self.table.setItem(current_row, col, QTableWidgetItem(value))
            
        # 取消选中状态
        checkbox = self.table.cellWidget(current_row, 0)
        if checkbox:
            checkbox.setChecked(False)
            
        # 恢复按钮状态
        for btn in self.findChildren(QPushButton):
            if btn.text() == "保存":
                btn.setText("增加")
                btn.clicked.disconnect()
                btn.clicked.connect(self.on_add_clicked)
        
        # 清空输入框和编辑状态
        self.clear_inputs()
        self.editing_row = None
        
    def on_delete_clicked(self):
        """处理删除按钮点击事件"""
        # 获取选中的行
        selected_rows = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)
        
        # 检查是否有选中的行
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请选择要删除的行！")
            return
            
        # 确认删除
        reply = QMessageBox.question(self, "确认删除", 
                                   f"确定要删除选中的 {len(selected_rows)} 行数据吗？",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 从后向前删除，避免索引变化
            for row in sorted(selected_rows, reverse=True):
                self.table.removeRow(row)
                
            # 如果正在编辑状态，且删除的是正在编辑的行，则清空编辑状态
            if self.editing_row is not None and self.editing_row in selected_rows:
                self.clear_inputs()
                # 恢复按钮状态
                for btn in self.findChildren(QPushButton):
                    if btn.text() == "保存":
                        btn.setText("增加")
                        btn.clicked.disconnect()
                        btn.clicked.connect(self.on_add_clicked)
                self.editing_row = None
        
    def clear_inputs(self):
        """清空所有输入框"""
        self.b_input.clear()
        self.l_input.clear()
        self.h_input.clear()
        self.x_input.clear()
        self.y_input.clear()
        self.h2_input.clear() 

    def dms_to_decimal(self, dms_str):
        """将度分秒格式转换为十进制度"""
        try:
            parts = dms_str.split(':')
            if len(parts) != 3:
                raise ValueError("Invalid DMS format")
            
            degrees = float(parts[0])
            minutes = float(parts[1])
            seconds = float(parts[2])
            
            # 处理负数情况
            sign = -1 if degrees < 0 else 1
            decimal = abs(degrees) + minutes/60 + seconds/3600
            return sign * decimal
        except Exception as e:
            raise ValueError(f"度分秒格式转换错误: {dms_str}")

    def get_coordinate_value(self, row, col):
        """获取表格中的坐标值，自动处理度分秒格式"""
        value = self.table.item(row, col).text()
        if ':' in value:  # 度分秒格式
            return self.dms_to_decimal(value)
        return float(value)

    def on_calculate_clicked(self):
        """处理计算按钮点击事件"""
        # 获取选中的行
        selected_rows = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)
        
        # 检查选中的点数是否足够
        if len(selected_rows) < 3:
            QMessageBox.warning(self, "提示", "七参数计算至少需要3个公共点！")
            return
        
        try:
            # 获取源坐标系和目标坐标系的类型
            source_is_blh = self.blh_radio1.isChecked()
            target_is_blh = self.blh_radio2.isChecked()
            source_system = "WGS84" if "WGS-84" in self.coord_system1.currentText() else "Beijing54"
            target_system = "WGS84" if "WGS-84" in self.coord_system2.currentText() else "Beijing54"
            
            # 准备源坐标和目标坐标数组
            source_coords = []
            target_coords = []
            
            for row in selected_rows:
                # 读取源坐标
                source_values = [self.get_coordinate_value(row, i) for i in range(1, 4)]
                # 读取目标坐标
                target_values = [self.get_coordinate_value(row, i) for i in range(4, 7)]
                print("【七参数转换】读取表格源数据：", source_values)
                print("【七参数转换】读取表格目标数据：", target_values)
                
                # 如果是BLH格式，需要转换为XYZ
                if source_is_blh:
                    # 只对经纬度转换为弧度，高程保持不变
                    source_values = [np.radians(source_values[0]), np.radians(source_values[1]), source_values[2]]
                    print("【七参数转换】源坐标（BLH）转换为弧度：", source_values)
                    # 根据坐标系选择转换函数
                    if source_system == "WGS84":
                        source_xyz = WGS84_BLH2XYZ(*source_values)
                    else:
                        source_xyz = Beijing54_BLH2XYZ(*source_values)
                    source_coords.append(source_xyz)
                else:
                    source_coords.append(source_values)
                
                if target_is_blh:
                    # 只对经纬度转换为弧度，高程保持不变
                    target_values = [np.radians(target_values[0]), np.radians(target_values[1]), target_values[2]]
                    # 根据坐标系选择转换函数
                    if target_system == "WGS84":
                        print("【七参数转换】目标坐标（BLH）转换为弧度：", target_values)
                        target_xyz = WGS84_BLH2XYZ(*target_values)
                    else:
                        target_xyz = Beijing54_BLH2XYZ(*target_values)
                    target_coords.append(target_xyz)
                else:
                    target_coords.append(target_values)
            
            # 转换为numpy数组
            source_coords = np.array(source_coords)
            target_coords = np.array(target_coords)

            print("【七参数转换】转换后的源坐标（XYZ）：\n", source_coords)
            print("【七参数转换】转换后的目标坐标（XYZ）：\n", target_coords)
            
            # 计算七参数
            result = bursa_seven_parameters(source_coords, target_coords)
            
            # 显示结果
            params = result['parameters']
            
            # 更新结果显示
            result_names = ['dx_result', 'dy_result', 'dz_result', 
                           'wx_result', 'wy_result', 'wz_result', 'k_result']
            for i, name in enumerate(result_names):
                widget = self.findChild(QLineEdit, name)
                if widget:
                    if i < 3:  # DX, DY, DZ显示为米
                        widget.setText(f"{params[i]:.8f} m")
                    elif i < 6:  # WX, WY, WZ显示为弧度
                        widget.setText(f"{params[i]:.8f} rad")
                    else:  # K显示为m
                        widget.setText(f"{params[i]:.8f} m")
            
            # 更新表格中的RMS值
            for i, row in enumerate(selected_rows):
                rms = np.sqrt(np.sum(result['residuals'][i]**2))
                self.table.setItem(row, 7, QTableWidgetItem(f"{rms:.4f}"))
            
            QMessageBox.information(self, "计算完成", "七参数计算完成！")
            
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"计算过程中发生错误：{str(e)}") 

    def on_header_clicked(self, logicalIndex):
        """处理表头点击事件"""
        # 只处理第一列（选择列）的点击
        if logicalIndex == 0:
            # 检查是否有数据行
            if self.table.rowCount() == 0:
                return
                
            # 判断当前是否所有行都已选中
            all_selected = True
            for row in range(self.table.rowCount()):
                checkbox = self.table.cellWidget(row, 0)
                if checkbox and not checkbox.isChecked():
                    all_selected = False
                    break
            
            # 所有都选中时则取消全选，否则进行全选    
            for row in range(self.table.rowCount()):
                checkbox = self.table.cellWidget(row, 0)
                if checkbox:
                    checkbox.setChecked(not all_selected)
        
    def update_select_all_state(self):
        """根据当前所有行复选框的状态更新全选复选框状态"""
        row_count = self.table.rowCount()
        if row_count == 0:
            self.select_all_checkbox.setChecked(False)
            return
            
        checked_count = 0
        for row in range(row_count):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                checked_count += 1
                
        # 临时阻断信号，避免触发toggle_all_checkboxes
        self.select_all_checkbox.blockSignals(True)
                
        # 如果所有行都被选中，则全选复选框为选中状态
        if checked_count == row_count:
            self.select_all_checkbox.setChecked(True)
        # 如果没有行被选中，则全选复选框为非选中状态
        else:
            self.select_all_checkbox.setChecked(False)
            
        # 恢复信号
        self.select_all_checkbox.blockSignals(False) 