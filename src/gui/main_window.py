from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QTabWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QTableWidgetItem, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QFontDatabase

from .pages.seven_param_page import SevenParamPage
from .pages.four_param_page import FourParamPage
from .pages.transform_page import TransformPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("坐标转换系统")
        self.setMinimumSize(1000, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
        self.old_pos = None
        self.setup_ui()
        self.setup_style()

    def setup_ui(self):
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建标题栏
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        # 标题
        title_label = QLabel("坐标转换系统")
        title_label.setObjectName("titleLabel")
        
        # 添加导入按钮
        import_button = QPushButton("导入JSON")
        import_button.setObjectName("importButton")
        import_button.clicked.connect(self.on_import_clicked)
        import_button.setFixedSize(100, 30)
        
        # 添加保存配置按钮和下拉菜单
        save_button = QPushButton("保存配置")
        save_button.setObjectName("importButton")
        save_button.clicked.connect(self.on_save_clicked)
        save_button.setFixedSize(100, 30)
        
        self.param_type_combo = QComboBox()
        self.param_type_combo.setObjectName("paramTypeCombo")
        self.param_type_combo.addItems(["七参数", "四参数"])
        self.param_type_combo.setFixedSize(100, 30)
        
        # 关闭按钮
        close_button = QPushButton("×")
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.close)
        close_button.setFixedSize(40, 40)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(import_button)  # 添加导入按钮
        title_layout.addWidget(save_button)    # 添加保存按钮
        title_layout.addWidget(self.param_type_combo)  # 添加下拉菜单
        title_layout.addWidget(close_button)
        
        # 创建内容区
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("mainTab")
        
        # 添加各个页面
        self.tab_widget.addTab(SevenParamPage(), "计算七参数")
        self.tab_widget.addTab(FourParamPage(), "计算四参数")
        self.tab_widget.addTab(TransformPage(), "转换坐标")
        
        content_layout.addWidget(self.tab_widget)
        
        # 添加到主布局
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_widget)

    def setup_style(self):
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background: transparent;
            }
            #titleBar {
                background-color: #1B2A4A;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                height: 45px;
            }
            #titleLabel {
                color: white;
                font-family: 'Microsoft YaHei UI';
                font-size: 20px;
                font-weight: 900;
            }
            #closeButton {
                background: transparent;
                border: none;
                color: white;
                font-family: 'Microsoft YaHei UI';
                font-size: 22px;
            }
            #closeButton:hover {
                background-color: #ff4d4d;
                color: white;
            }
            #contentWidget {
                background-color: #FFFFFF;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            #mainTab > QTabBar::tab {
                padding: 12px 0px;
                margin: 5px 3px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #3B7EA1, stop:1 #2FA698);
                border: none;
                border-radius: 8px;
                color: white;
                font-family: 'Microsoft YaHei UI';
                font-size: 18px;
                font-weight: 800;
                min-width: 150px;
                text-align: center;
                height: 20px;
                line-height: 20px;
            }
            #mainTab > QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2C5F8C, stop:1 #25867B);
                font-weight: 900;
            }
            #mainTab > QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #346D95, stop:1 #2A998C);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #3B7EA1, stop:1 #2FA698);
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                color: white;
                font-family: 'Microsoft YaHei UI';
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #346D95, stop:1 #2A998C);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2C5F8C, stop:1 #25867B);
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E6ED;
                border-radius: 8px;
                gridline-color: #E0E6ED;
                font-family: 'Microsoft YaHei UI';
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #E7F2F5;
                color: #2C5F8C;
            }
            QHeaderView::section {
                background-color: #F5F8FA;
                padding: 8px;
                border: none;
                border-right: 1px solid #E0E6ED;
                border-bottom: 1px solid #E0E6ED;
                font-family: 'Microsoft YaHei UI';
                font-weight: bold;
                color: #2C5F8C;
            }
            QLabel {
                color: #2C5F8C;
                font-family: 'Microsoft YaHei UI';
                font-size: 14px;
            }
            #paramTypeCombo {
                background: transparent;
                border: 1px solid white;
                color: white;
                font-family: 'Microsoft YaHei UI';
                font-size: 14px;
                padding: 6px 10px;
                border-radius: 6px;
                min-width: 100px;
            }
            
            #paramTypeCombo:hover {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid #BBDEFB;
            }
            
            #paramTypeCombo:focus {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid #2196F3;
            }
            
            #paramTypeCombo::drop-down {
                border: none;
                width: 20px;
            }
            
            #paramTypeCombo::down-arrow {
                image: url(resources/down_arrow.png);
                width: 12px;
                height: 12px;
            }
            
            #paramTypeCombo QAbstractItemView {
                border: 1px solid #1B2A4A;
                border-radius: 4px;
                background-color: #1B2A4A;
                color: white;
                selection-background-color: #3B7EA1;
                selection-color: white;
                padding: 4px;
            }
        """)
        
        # 添加导入按钮的样式
        self.setStyleSheet(self.styleSheet() + """
            #importButton {
                background: transparent;
                border: 1px solid white;
                color: white;
                font-family: 'Microsoft YaHei UI';
                font-size: 14px;
                padding: 5px 15px;
            }
            #importButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            #importButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def on_import_clicked(self):
        """处理导入按钮点击事件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择JSON文件",
            "",
            "JSON Files (*.json);;Text Files (*.txt)"
        )
        if file_path:
            try:
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 根据config_type确定导入到哪个页面
                config_type = data.get('config_type', '七参数')  # 默认为七参数
                
                # 根据不同参数类型分别处理
                if config_type == '七参数':
                    self._import_seven_param_data(data)
                elif config_type == '四参数':
                    self._import_four_param_data(data)
                else:
                    # 默认处理为七参数
                    self._import_seven_param_data(data)
                
                QMessageBox.information(self, "导入成功", f"{config_type}数据已成功导入！")
                
            except Exception as e:
                QMessageBox.critical(self, "导入错误", f"导入过程中发生错误：{str(e)}")
    
    def _import_seven_param_data(self, data):
        """导入七参数数据"""
        # 切换到七参数页面
        page_index = 0
        self.tab_widget.setCurrentIndex(page_index)
        param_page = self.tab_widget.widget(page_index)
        
        # 清空现有表格数据
        param_page.table.setRowCount(0)
        
        # 处理坐标系信息
        if 'source_coordinate' in data and 'target_coordinate' in data:
            # 设置源坐标系和目标坐标系的类型
            source_type = data['source_coordinate']['type']
            target_type = data['target_coordinate']['type']
            
            # 设置坐标系选择
            if source_type == 'BLH':
                param_page.blh_radio1.setChecked(True)
                param_page.xyz_radio1.setChecked(False)
            else:
                param_page.blh_radio1.setChecked(False)
                param_page.xyz_radio1.setChecked(True)
                
            if target_type == 'BLH':
                param_page.blh_radio2.setChecked(True)
                param_page.xyz_radio2.setChecked(False)
            else:
                param_page.blh_radio2.setChecked(False)
                param_page.xyz_radio2.setChecked(True)
            
            # 设置单位格式
            source_unit = data['source_coordinate']['unit']
            target_unit = data['target_coordinate']['unit']
            param_page.unit_combo1.setCurrentText(source_unit)
            param_page.unit_combo2.setCurrentText(target_unit)
            
            # 设置参考系统
            source_system = data['source_coordinate']['reference_system']
            target_system = data['target_coordinate']['reference_system']
            param_page.coord_system1.setCurrentText(source_system + "坐标系")
            param_page.coord_system2.setCurrentText(target_system + "坐标系")
            
            # 导入坐标点数据
            source_points = data['source_coordinate']['points']
            target_points = data['target_coordinate']['points']
            
            for i in range(len(source_points)):
                row = param_page.table.rowCount()
                param_page.table.insertRow(row)
                
                # 添加复选框
                from PyQt5.QtWidgets import QCheckBox
                checkbox = QCheckBox()
                param_page.table.setCellWidget(row, 0, checkbox)
                
                # 添加源坐标
                if source_type == 'BLH':
                    param_page.table.setItem(row, 1, QTableWidgetItem(str(source_points[i]['B'])))
                    param_page.table.setItem(row, 2, QTableWidgetItem(str(source_points[i]['L'])))
                    param_page.table.setItem(row, 3, QTableWidgetItem(str(source_points[i]['H'])))
                else:
                    param_page.table.setItem(row, 1, QTableWidgetItem(str(source_points[i]['X'])))
                    param_page.table.setItem(row, 2, QTableWidgetItem(str(source_points[i]['Y'])))
                    param_page.table.setItem(row, 3, QTableWidgetItem(str(source_points[i]['Z'])))
                
                # 添加目标坐标
                if target_type == 'BLH':
                    param_page.table.setItem(row, 4, QTableWidgetItem(str(target_points[i]['B'])))
                    param_page.table.setItem(row, 5, QTableWidgetItem(str(target_points[i]['L'])))
                    param_page.table.setItem(row, 6, QTableWidgetItem(str(target_points[i]['H'])))
                else:
                    param_page.table.setItem(row, 4, QTableWidgetItem(str(target_points[i]['X'])))
                    param_page.table.setItem(row, 5, QTableWidgetItem(str(target_points[i]['Y'])))
                    param_page.table.setItem(row, 6, QTableWidgetItem(str(target_points[i]['Z'])))
                
                # 如果有RMS值，添加RMS
                if 'rms_values' in data and i < len(data['rms_values']):
                    rms = data['rms_values'][i].get('rms')
                    if rms is not None:
                        param_page.table.setItem(row, 7, QTableWidgetItem(str(rms)))
        
        # 设置七参数值
        if 'transformation_parameters' in data:
            params = data['transformation_parameters']
            
            # 根据页面显示逻辑设置参数值
            if params.get('DX') is not None:
                param_page.findChild(QLineEdit, 'dx_result').setText(f"{params['DX']:.8f} m")
            if params.get('DY') is not None:
                param_page.findChild(QLineEdit, 'dy_result').setText(f"{params['DY']:.8f} m")
            if params.get('DZ') is not None:
                param_page.findChild(QLineEdit, 'dz_result').setText(f"{params['DZ']:.8f} m")
            if params.get('WX') is not None:
                param_page.findChild(QLineEdit, 'wx_result').setText(f"{params['WX']:.8f} rad")
            if params.get('WY') is not None:
                param_page.findChild(QLineEdit, 'wy_result').setText(f"{params['WY']:.8f} rad")
            if params.get('WZ') is not None:
                param_page.findChild(QLineEdit, 'wz_result').setText(f"{params['WZ']:.8f} rad")
            if params.get('K') is not None:
                param_page.findChild(QLineEdit, 'k_result').setText(f"{params['K']:.8f} m")
    
    def _import_four_param_data(self, data):
        """导入四参数数据"""
        # 切换到四参数页面
        page_index = 1
        self.tab_widget.setCurrentIndex(page_index)
        param_page = self.tab_widget.widget(page_index)
        
        # 清空现有表格数据
        param_page.table.setRowCount(0)
        
        # 设置椭球基准
        if 'source_coordinate' in data and 'reference_system' in data['source_coordinate']:
            reference_system = data['source_coordinate']['reference_system']
            index = param_page.ellipsoid_combo.findText(reference_system)
            if index >= 0:
                param_page.ellipsoid_combo.setCurrentIndex(index)
        
        # 处理坐标点数据
        if 'source_coordinate' in data and 'target_coordinate' in data:
            source_points = data['source_coordinate'].get('points', [])
            target_points = data['target_coordinate'].get('points', [])
            
            # 确保数据按ID排序
            source_dict = {point.get('id', i+1): point for i, point in enumerate(source_points)}
            target_dict = {point.get('id', i+1): point for i, point in enumerate(target_points)}
            
            # 获取所有ID
            all_ids = sorted(set(list(source_dict.keys()) + list(target_dict.keys())))
            
            for id_value in all_ids:
                if id_value in source_dict and id_value in target_dict:
                    src_point = source_dict[id_value]
                    tgt_point = target_dict[id_value]
                    
                    row = param_page.table.rowCount()
                    param_page.table.insertRow(row)
                    
                    # 添加复选框
                    from PyQt5.QtWidgets import QCheckBox
                    checkbox = QCheckBox()
                    checkbox.stateChanged.connect(param_page.update_select_all_state)
                    param_page.table.setCellWidget(row, 0, checkbox)
                    
                    # 添加源坐标
                    source_x = src_point.get('X', '')
                    source_y = src_point.get('Y', '')
                    param_page.table.setItem(row, 1, QTableWidgetItem(str(source_x)))
                    param_page.table.setItem(row, 2, QTableWidgetItem(str(source_y)))
                    
                    # 添加目标坐标
                    target_x = tgt_point.get('X', '')
                    target_y = tgt_point.get('Y', '')
                    param_page.table.setItem(row, 3, QTableWidgetItem(str(target_x)))
                    param_page.table.setItem(row, 4, QTableWidgetItem(str(target_y)))
            
            # 添加RMS值
            if 'rms_values' in data:
                rms_dict = {item.get('point_id', i+1): item.get('rms') 
                           for i, item in enumerate(data['rms_values'])}
                
                for row in range(param_page.table.rowCount()):
                    point_id = row + 1
                    if point_id in rms_dict and rms_dict[point_id] is not None:
                        if param_page.table.columnCount() > 5:
                            param_page.table.setItem(row, 5, QTableWidgetItem(str(rms_dict[point_id])))
        
        # 设置四参数值
        if 'transformation_parameters' in data:
            params = data['transformation_parameters']
            
            # 根据模板中的参数名称和格式设置参数值
            if params.get('a') is not None:
                param_page.findChild(QLineEdit, 'a_result').setText(f"{params['a']}")
            if params.get('b') is not None:
                param_page.findChild(QLineEdit, 'b_result').setText(f"{params['b']}")
            if params.get('dx') is not None:
                param_page.findChild(QLineEdit, 'dx_result').setText(f"{params['dx']}")
            if params.get('dy') is not None:
                param_page.findChild(QLineEdit, 'dy_result').setText(f"{params['dy']}")
            if params.get('s') is not None:
                param_page.findChild(QLineEdit, 's_result').setText(f"{params['s']}")
            if params.get('θ') is not None:
                # 角度参数可能需要添加单位
                param_page.findChild(QLineEdit, 'theta_result').setText(f"{params['θ']} rad")

    def on_save_clicked(self):
        """处理保存配置按钮点击事件"""
        param_type = self.param_type_combo.currentText()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存配置文件",
            "",
            "JSON Files (*.json)"
        )
        if file_path:
            try:
                # 根据不同参数类型调用不同的保存函数
                if param_type == "七参数":
                    self._save_seven_param_data(file_path)
                elif param_type == "四参数":
                    self._save_four_param_data(file_path)
                else:
                    raise ValueError(f"未知的参数类型：{param_type}")
                
                QMessageBox.information(self, "保存成功", f"{param_type}配置信息已成功保存！")
            except Exception as e:
                QMessageBox.critical(self, "保存错误", f"保存过程中发生错误：{str(e)}")
    
    def _save_seven_param_data(self, file_path):
        """专门保存七参数数据为JSON文件
        
        Args:
            file_path: 保存的文件路径
        """
        import json
        
        # 获取七参数页面
        page_index = 0
        page = self.tab_widget.widget(page_index)
        
        # 创建JSON数据结构，符合七参数模板格式
        data = {
            "config_type": "七参数",
            "source_coordinate": {},
            "target_coordinate": {},
            "transformation_parameters": {},
            "rms_values": []
        }
        
        # 获取源坐标系和目标坐标系的类型
        source_is_blh = page.blh_radio1.isChecked()
        target_is_blh = page.blh_radio2.isChecked()
        
        # 设置坐标系类型
        data["source_coordinate"]["type"] = "BLH" if source_is_blh else "XYZ"
        data["target_coordinate"]["type"] = "BLH" if target_is_blh else "XYZ"
        
        # 获取单位
        data["source_coordinate"]["unit"] = page.unit_combo1.currentText()
        data["target_coordinate"]["unit"] = page.unit_combo2.currentText()
        
        # 获取参考系统
        source_system = page.coord_system1.currentText().replace("坐标系", "")
        target_system = page.coord_system2.currentText().replace("坐标系", "")
        data["source_coordinate"]["reference_system"] = source_system
        data["target_coordinate"]["reference_system"] = target_system
        
        # 获取坐标点数据
        source_points = []
        target_points = []
        rms_values = []
        
        row_count = page.table.rowCount()
        for row in range(row_count):
            # 获取源坐标
            source_point = {"id": row + 1}
            if source_is_blh:
                source_point["B"] = page.table.item(row, 1).text() if page.table.item(row, 1) else ""
                source_point["L"] = page.table.item(row, 2).text() if page.table.item(row, 2) else ""
                source_point["H"] = page.table.item(row, 3).text() if page.table.item(row, 3) else ""
            else:
                source_point["X"] = page.table.item(row, 1).text() if page.table.item(row, 1) else ""
                source_point["Y"] = page.table.item(row, 2).text() if page.table.item(row, 2) else ""
                source_point["Z"] = page.table.item(row, 3).text() if page.table.item(row, 3) else ""
            
            # 获取目标坐标
            target_point = {"id": row + 1}
            if target_is_blh:
                target_point["B"] = page.table.item(row, 4).text() if page.table.item(row, 4) else ""
                target_point["L"] = page.table.item(row, 5).text() if page.table.item(row, 5) else ""
                target_point["H"] = page.table.item(row, 6).text() if page.table.item(row, 6) else ""
            else:
                target_point["X"] = page.table.item(row, 4).text() if page.table.item(row, 4) else ""
                target_point["Y"] = page.table.item(row, 5).text() if page.table.item(row, 5) else ""
                target_point["Z"] = page.table.item(row, 6).text() if page.table.item(row, 6) else ""
            
            # 获取RMS值
            rms_value = {"point_id": row + 1}
            if page.table.columnCount() > 7 and page.table.item(row, 7):
                rms_value["rms"] = page.table.item(row, 7).text()
            else:
                rms_value["rms"] = None
            
            source_points.append(source_point)
            target_points.append(target_point)
            rms_values.append(rms_value)
        
        data["source_coordinate"]["points"] = source_points
        data["target_coordinate"]["points"] = target_points
        data["rms_values"] = rms_values
        
        # 获取七参数值
        try:
            data["transformation_parameters"] = {
                "DX": float(page.findChild(QLineEdit, 'dx_result').text().split()[0]) if page.findChild(QLineEdit, 'dx_result').text() else None,
                "DY": float(page.findChild(QLineEdit, 'dy_result').text().split()[0]) if page.findChild(QLineEdit, 'dy_result').text() else None,
                "DZ": float(page.findChild(QLineEdit, 'dz_result').text().split()[0]) if page.findChild(QLineEdit, 'dz_result').text() else None,
                "WX": float(page.findChild(QLineEdit, 'wx_result').text().split()[0]) if page.findChild(QLineEdit, 'wx_result').text() else None,
                "WY": float(page.findChild(QLineEdit, 'wy_result').text().split()[0]) if page.findChild(QLineEdit, 'wy_result').text() else None,
                "WZ": float(page.findChild(QLineEdit, 'wz_result').text().split()[0]) if page.findChild(QLineEdit, 'wz_result').text() else None,
                "K": float(page.findChild(QLineEdit, 'k_result').text().split()[0])  if page.findChild(QLineEdit, 'k_result').text() else None
            }
        except (IndexError, ValueError, AttributeError):
            # 如果获取失败，设置为空值
            data["transformation_parameters"] = {
                "DX": None, "DY": None, "DZ": None,
                "WX": None, "WY": None, "WZ": None, "K": None
            }
        
        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _save_four_param_data(self, file_path):
        """专门保存四参数数据为JSON文件
        
        Args:
            file_path: 保存的文件路径
        """
        import json
        
        # 获取四参数页面
        page_index = 1  # 四参数页面索引为1
        page = self.tab_widget.widget(page_index)
        
        # 创建JSON数据结构，符合四参数模板格式
        data = {
            "config_type": "四参数",
            "source_coordinate": {
                "type": "平面直角坐标",
                "unit": "米",
                "reference_system": page.ellipsoid_combo.currentText(),
                "points": []
            },
            "target_coordinate": {
                "type": "平面直角坐标",
                "unit": "米",
                "reference_system": page.ellipsoid_combo.currentText(),
                "points": []
            },
            "transformation_parameters": {},
            "rms_values": []
        }
        
        # 获取坐标点数据
        source_points = []
        target_points = []
        rms_values = []
        
        row_count = page.table.rowCount()
        for row in range(row_count):
            # 获取源坐标 (X, Y)
            source_point = {"id": row + 1}
            source_point["X"] = page.table.item(row, 1).text() if page.table.item(row, 1) else ""
            source_point["Y"] = page.table.item(row, 2).text() if page.table.item(row, 2) else ""
            
            # 获取目标坐标 (X, Y)
            target_point = {"id": row + 1}
            target_point["X"] = page.table.item(row, 3).text() if page.table.item(row, 3) else ""
            target_point["Y"] = page.table.item(row, 4).text() if page.table.item(row, 4) else ""
            
            # 获取RMS值 (如果有)
            rms_value = {"point_id": row + 1}
            if page.table.columnCount() > 5 and page.table.item(row, 5):
                rms_value["rms"] = page.table.item(row, 5).text()
            else:
                rms_value["rms"] = None
            
            source_points.append(source_point)
            target_points.append(target_point)
            rms_values.append(rms_value)
        
        data["source_coordinate"]["points"] = source_points
        data["target_coordinate"]["points"] = target_points
        data["rms_values"] = rms_values
        
        # 获取四参数值
        try:
            data["transformation_parameters"] = {
                "a": float(page.findChild(QLineEdit, 'a_result').text()) if page.findChild(QLineEdit, 'a_result').text() else None,
                "b": float(page.findChild(QLineEdit, 'b_result').text()) if page.findChild(QLineEdit, 'b_result').text() else None,
                "dx": float(page.findChild(QLineEdit, 'dx_result').text()) if page.findChild(QLineEdit, 'dx_result').text() else None,
                "dy": float(page.findChild(QLineEdit, 'dy_result').text()) if page.findChild(QLineEdit, 'dy_result').text() else None,
                "s": float(page.findChild(QLineEdit, 's_result').text()) if page.findChild(QLineEdit, 's_result').text() else None,
                "θ": float(page.findChild(QLineEdit, 'theta_result').text().split()[0]) if page.findChild(QLineEdit, 'theta_result').text() else None
            }
        except (IndexError, ValueError, AttributeError) as e:
            # 如果获取失败，记录错误并设置为空值
            print(f"获取四参数值出错: {str(e)}")
            data["transformation_parameters"] = {
                "a": None, "b": None, "dx": None, "dy": None, "s": None, "θ": None
            }
        
        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
