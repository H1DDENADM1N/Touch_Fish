import sys

import keyboard
import psutil
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QCompleter,
    QLabel,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)
from .utils.cosmic import __icon_path__
from .utils.hide_window import hide_window
from .utils.restore_window import restore_window

__hide_hotkey__ = "alt+z"
__restore_hotkey__ = "alt+x"


class WindowController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Touch Fish")
        self.setWindowIcon(QIcon(str(__icon_path__)))
        self.setGeometry(100, 100, 300, 150)

        self.create_widgets()  # 创建图形界面组件

        self.create_tray_icon()  # 创建系统托盘图标

        self.bind_hotkeys()  # 设置快捷键

        self.update_process_list()  # 更新进程列表

    def create_widgets(self):
        layout = QVBoxLayout()

        # 创建进程选择标签
        self.process_label = QLabel("Select Process:")
        layout.addWidget(self.process_label)

        # 创建进程选择下拉列表
        self.process_dropdown = QComboBox()
        self.process_dropdown.setEditable(True)  # 设置为可编辑以启用搜索
        completer = QCompleter(self.process_dropdown.model())
        completer.setCaseSensitivity(Qt.CaseInsensitive)  # 不区分大小写
        self.process_dropdown.setCompleter(completer)
        layout.addWidget(self.process_dropdown)

        # 创建 隐藏/恢复 复选框
        self.hide_or_restore_checkbox = QCheckBox("Hide")
        font = self.hide_or_restore_checkbox.font()
        font.setPointSize(18)
        self.hide_or_restore_checkbox.setFont(font)
        self.hide_or_restore_checkbox.stateChanged.connect(
            lambda: self.hide_process()
            if self.hide_or_restore_checkbox.isChecked()
            else self.restore_process()
        )
        layout.addWidget(self.hide_or_restore_checkbox)

        # 创建刷新进程列表按钮
        self.refresh_button = QPushButton("Refresh Process List")
        self.refresh_button.clicked.connect(self.update_process_list)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

    def create_tray_icon(self):
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(QIcon(str(__icon_path__)), parent=self)
        self.tray_icon.setToolTip("Touch Fish")
        self.tray_icon.activated.connect(
            lambda: self.showNormal() if self.isHidden() else self.hide()
        )

        # 创建菜单
        menu = QMenu()
        show_action = QAction("显示", self)
        show_action.triggered.connect(lambda: self.showNormal())
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(lambda: QApplication.quit())
        menu.addAction(show_action)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def bind_hotkeys(self):
        # 设置快捷键
        keyboard.add_hotkey(__hide_hotkey__, self.hide_process)
        keyboard.add_hotkey(__restore_hotkey__, self.restore_process)

    def update_process_list(self):
        # 更新进程列表
        processes = [proc.name() for proc in psutil.process_iter(["pid", "name"])]
        self.process_dropdown.clear()
        self.process_dropdown.addItems(list(set(processes)))

    def hide_process(self):
        # 隐藏选定进程的窗口
        process_name = self.process_dropdown.currentText()
        if process_name:
            hide_window(process_name)

    def restore_process(self):
        # 恢复选定进程的窗口
        process_name = self.process_dropdown.currentText()
        if process_name:
            restore_window(process_name)

    def closeEvent(self, event):
        # 不关闭应用程序，隐藏主窗口
        self.hide()
        event.ignore()


def main():
    app = QApplication(sys.argv)
    window = WindowController()
    window.show()
    sys.exit(app.exec())
