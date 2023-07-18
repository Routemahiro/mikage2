# ActiveWindowTracker.py
import pygetwindow as gw
from datetime import datetime
from controllers.pomodoro_db_controller import PomodoroDBController
import time


class ActiveWindowTracker:
    def __init__(self, db_controller: PomodoroDBController, session_id):
        self.db_controller = db_controller
        self.session_id = session_id
        self.is_tracking = False

    def get_active_window_title(self):
        # アクティブウィンドウの取得
        window = gw.getActiveWindow()

        # ウィンドウが見つからなかった場合のエラーハンドリング
        if window == None:
            return "No Active Window"
        else:
            return window.title

    def start_tracking(self):
        self.is_tracking = True
        while self.is_tracking:
            title = self.get_active_window_title()
            if title:
                self.db_controller.add_window_activity(self.session_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), title)
            time.sleep(60)

    def stop_tracking(self):
        self.is_tracking = False


# import win32gui
# import win32process
# import psutil
# from datetime import datetime
# from controllers.pomodoro_db_controller import PomodoroDBController
# import time

# class ActiveWindowTracker:
#     def __init__(self, db_controller: PomodoroDBController, session_id):
#         self.db_controller = db_controller
#         self.session_id = session_id
#         self.is_tracking = False

#     def get_active_window_pid(self):
#         hwnd = win32gui.GetForegroundWindow()  # アクティブなウィンドウのハンドルを取得
#         _, pid = win32process.GetWindowThreadProcessId(hwnd)  # ウィンドウのスレッドIDとプロセスIDを取得
#         return pid

#     def get_program_name(self, pid):
#         process = psutil.Process(pid)
#         return process.name()

#     def start_tracking(self):
#         self.is_tracking = True
#         while self.is_tracking:
#             pid = self.get_active_window_pid()
#             program_name = self.get_program_name(pid)
#             if program_name:
#                 self.db_controller.add_window_activity(self.session_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), program_name)
#             time.sleep(60)

#     def stop_tracking(self):
#         self.is_tracking = False
