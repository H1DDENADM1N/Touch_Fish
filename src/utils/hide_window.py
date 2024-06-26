import psutil
import win32gui
import win32process
import win32con
from .cosmic import original_styles


def hide_window(process_name):
    # 隐藏指定进程的所有窗口
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.name() == process_name:
            pid = proc.info["pid"]
            hide_window_by_pid(pid)


def hide_window_by_pid(pid):
    # 隐藏指定进程ID的所有窗口

    def callback(hwnd, whdls):
        if win32gui.IsWindowVisible(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                whdls.append(hwnd)
                original_styles[hwnd] = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                win32gui.ShowWindow(hwnd, 0)
                win32gui.SetWindowLong(
                    hwnd,
                    win32con.GWL_STYLE,
                    original_styles[hwnd] & ~win32con.WS_VISIBLE,
                )

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
