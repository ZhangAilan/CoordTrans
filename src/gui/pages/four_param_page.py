from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                           QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                           QLineEdit, QGroupBox, QMessageBox, QCheckBox, QComboBox)
from PyQt5.QtCore import Qt
import numpy as np
from function.four_par import calculate_four_parameters

class FourParamPage(QWidget):
    def __init__(self):
        super().__init__()
        self.editing_row = None  # 添加编辑行的标记
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 添加椭球基准选择区域
        ellipsoid_layout = QHBoxLayout()
        ellipsoid_label = QLabel("椭球基准:")
        self.ellipsoid_combo = QComboBox()
        self.ellipsoid_combo.addItems(["WGS84", "北京54"])
        self.ellipsoid_combo.setFixedWidth(200)
        
        ellipsoid_layout.addWidget(ellipsoid_label)
        ellipsoid_layout.addWidget(self.ellipsoid_combo)
        ellipsoid_layout.addStretch()
        
        # 创建上部分布局
        top_layout = QHBoxLayout()
        
        # 源坐标系组
        source_group = QGroupBox("输入源坐标")
        source_layout = QGridLayout()
        
        # 添加源坐标系控件
        self.x0_label = QLabel("X0=")
        self.y0_label = QLabel("Y0=")
        
        self.x0_input = QLineEdit()
        self.y0_input = QLineEdit()
        
        # 布局源坐标系控件
        source_layout.addWidget(self.x0_label, 0, 0)
        source_layout.addWidget(self.x0_input, 0, 1)
        source_layout.addWidget(self.y0_label, 1, 0)
        source_layout.addWidget(self.y0_input, 1, 1)
        
        source_group.setLayout(source_layout)
        
        # 目标坐标系组
        target_group = QGroupBox("输入目标坐标")
        target_layout = QGridLayout()
        
        # 添加目标坐标系控件
        self.x1_label = QLabel("X1=")
        self.y1_label = QLabel("Y1=")
        
        self.x1_input = QLineEdit()
        self.y1_input = QLineEdit()
        
        # 布局目标坐标系控件
        target_layout.addWidget(self.x1_label, 0, 0)
        target_layout.addWidget(self.x1_input, 0, 1)
        target_layout.addWidget(self.y1_label, 1, 0)
        target_layout.addWidget(self.y1_input, 1, 1)
        
        target_group.setLayout(target_layout)
        
        # 结果组
        result_group = QGroupBox("计算结果")
        result_layout = QGridLayout()
        
        # 添加四参数结果显示
        params = [
            ("a:", "a_result"), ("b:", "b_result"), 
            ("dx:", "dx_result"), ("dy:", "dy_result"),
            ("s:", "s_result"), ("θ:", "theta_result")
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
        self.table.setColumnCount(5)
        headers = ["选择", "源坐标X", "源坐标Y", "目标坐标X", "目标坐标Y"]
        self.table.setHorizontalHeaderLabels(headers)
        
        # 设置表头点击信号连接
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        
        # 调整布局比例
        layout.addLayout(ellipsoid_layout)  # 添加椭球基准选择区域
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
            
            QLabel {
                font-family: 'Microsoft YaHei UI';
                font-size: 13px;
                color: #333333;
                padding: 4px;
            }
            
            QPushButton {
                min-width: 80px;
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
        """
        self.setStyleSheet(style)
        
    def validate_coordinate_format(self, value):
        """验证坐标格式"""
        try:
            value = float(value)
            return True
        except:
            return False
            
    def on_add_clicked(self):
        """处理增加按钮点击事件"""
        # 获取所有输入值
        source_values = [self.x0_input.text().strip(), self.y0_input.text().strip()]
        target_values = [self.x1_input.text().strip(), self.y1_input.text().strip()]
        
        # 检查是否有空值
        if any(not v for v in source_values + target_values):
            QMessageBox.warning(self, "输入错误", "所有字段都必须填写！")
            return
            
        # 验证坐标格式
        if not all(self.validate_coordinate_format(v) for v in source_values + target_values):
            QMessageBox.warning(self, "输入错误", "坐标必须是有效的数值！")
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
        source_values = [self.table.item(row, i).text() for i in range(1, 3)]
        target_values = [self.table.item(row, i).text() for i in range(3, 5)]
        
        # 设置源坐标值
        self.x0_input.setText(source_values[0])
        self.y0_input.setText(source_values[1])
        
        # 设置目标坐标值
        self.x1_input.setText(target_values[0])
        self.y1_input.setText(target_values[1])
        
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
            
        # 获取所有输入值并验证
        source_values = [self.x0_input.text().strip(), self.y0_input.text().strip()]
        target_values = [self.x1_input.text().strip(), self.y1_input.text().strip()]
        
        # 检查是否有空值
        if any(not v for v in source_values + target_values):
            QMessageBox.warning(self, "输入错误", "所有字段都必须填写！")
            return
            
        # 验证坐标格式
        if not all(self.validate_coordinate_format(v) for v in source_values + target_values):
            QMessageBox.warning(self, "输入错误", "坐标必须是有效的数值！")
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
        self.x0_input.clear()
        self.y0_input.clear()
        self.x1_input.clear()
        self.y1_input.clear()

    def on_calculate_clicked(self):
        """处理计算按钮点击事件"""
        # 获取选中的行
        selected_rows = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)
        
        # 检查选中的点数是否足够
        if len(selected_rows) < 2:
            QMessageBox.warning(self, "提示", "四参数计算至少需要2个公共点！")
            return
        
        try:
            # 准备源坐标和目标坐标列表
            source_points = []
            target_points = []
            
            for row in selected_rows:
                # 读取源坐标和目标坐标
                x0 = float(self.table.item(row, 1).text())
                y0 = float(self.table.item(row, 2).text())
                x1 = float(self.table.item(row, 3).text())
                y1 = float(self.table.item(row, 4).text())
                
                source_points.append((x0, y0))
                target_points.append((x1, y1))
            
            # 计算四参数
            params = calculate_four_parameters(source_points, target_points)
            
            # 更新结果显示
            self.findChild(QLineEdit, "a_result").setText(f"{params['a']:.8f}")
            self.findChild(QLineEdit, "b_result").setText(f"{params['b']:.8f}")
            self.findChild(QLineEdit, "dx_result").setText(f"{params['dx']:.8f}")
            self.findChild(QLineEdit, "dy_result").setText(f"{params['dy']:.8f}")
            self.findChild(QLineEdit, "s_result").setText(f"{params['s']:.8f}")
            self.findChild(QLineEdit, "theta_result").setText(f"{params['theta']:.8f} rad")
            
            QMessageBox.information(self, "计算完成", "四参数计算完成！")
            
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
        """更新选择状态"""
        # 由于没有全选复选框，这个方法在这个简化版本中可以留空
        pass 