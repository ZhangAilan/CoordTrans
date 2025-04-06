import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow

if __name__ == '__main__':
    # 直接指定虚拟环境中的插件路径
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
        os.path.dirname(os.path.dirname(sys.executable)),
        "Lib",
        "site-packages",
        "PyQt5",
        "Qt5",
        "plugins",
        "platforms"
    )
    
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())