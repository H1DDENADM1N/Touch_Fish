import win32gui
import win32con
import win32process
import psutil
from .cosmic import original_styles


def restore_window(process_name):
    # 恢复指定进程的所有窗口
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.name() == process_name:
            pid = proc.info["pid"]
            restore_window_by_pid(pid)


def restore_window_by_pid(pid):
    # 恢复指定进程ID的所有窗口
    def callback(hwnd, original_styles):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            original_style = original_styles.get(hwnd, None)
            if original_style is not None:
                win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, original_style)
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                win32gui.RedrawWindow(
                    hwnd,
                    None,
                    None,
                    win32con.RDW_INVALIDATE
                    | win32con.RDW_UPDATENOW
                    | win32con.RDW_ALLCHILDREN,
                )

    win32gui.EnumWindows(callback, original_styles)
