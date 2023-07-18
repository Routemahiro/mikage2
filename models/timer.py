# models.timer.py
from PySide6.QtCore import QObject, QTimer, Signal
from config_loader import load_config
from controllers.ai_controller import AIController

class Timer(QObject):

    updated = Signal()
    resetted = Signal(str)  # Updated to pass a string message

    def __init__(self):
        super(Timer, self).__init__()  # Important to call the parent class's init method
        config = load_config()
        self.duration = config["pomodoro_duration"] * 60  # duration minutes in seconds
        self.remaining_time = self.duration
        self.is_running = False
        self.ai = AIController()
        self.session_id = None

        self.qtimer = QTimer()
        self.qtimer.timeout.connect(self._update_remaining_time)

    def _update_remaining_time(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.reset()
        self.updated.emit()

    def start(self, tracker=None):
        self.is_running = True
        self.tracker = tracker  # Store tracker
        self.qtimer.start(1000)

    def pause(self):
        self.is_running = False
        self.qtimer.stop()

    # def reset(self):
    #     self.pause()
    #     if self.tracker:
    #         self.tracker.stop_tracking()
    #     self.remaining_time = self.duration
        
        
    #     self.resetted.emit() # Pass the message when emitting the signal

    def reset(self):
        self.pause()
        if self.tracker:
            self.tracker.stop_tracking()
        self.remaining_time = self.duration
        
        # Generate the session comment and emit it with the resetted signal
        session_comment = self.ai.generate_session_comment(self.session_id)
        self.resetted.emit(session_comment)



    def get_time_remaining(self):
        return self.remaining_time
