# timer_model.py
from PySide6.QtCore import QTime
from config_loader import load_config

class TimerModel:
    def __init__(self):
        config = load_config()
        self.pomodoro_time = QTime(0, config["pomodoro_duration"])
        self.break_time = QTime(0, 5)
        self.is_break_time = False
        self.remaining_time = self.pomodoro_time

    def reset(self):
        self.remaining_time = self.break_time if self.is_break_time else self.pomodoro_time
        self.is_break_time = not self.is_break_time
