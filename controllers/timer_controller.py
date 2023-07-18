# timer_controller.py
from PySide6.QtCore import QTimer, Slot
from models.timer_model import TimerModel
from views.countdowntimer_view import TimerView
from PySide6.QtCore import QTime
from controllers.ActiveWindowTracker import ActiveWindowTracker
from controllers.pomodoro_db_controller import PomodoroDBController
from datetime import datetime
from database.db_handler import DB_PATH
from models.timer import Timer
import threading
import atexit
from views.timer_view import create_textbox
from PySide6.QtWidgets import QApplication
from controllers.ai_controller import AIController

class TimerController:
    def __init__(self, db_controller, ai_controller):
        self.view = TimerView()
        self.model = TimerModel()
        self.ai = AIController()
        atexit.register(self.end_session)
        
        self.view.btn.clicked.connect(self.toggle_timer)
        
        # self.timer = QTimer()
        self.timer = Timer()
        self.timer.updated.connect(self.update_timer)
        self.timer.updated.connect(self.update_label)
        self.update_label()
        self.db_controller = PomodoroDBController(DB_PATH)

        self.db_controller = db_controller
        self.ai_controller = ai_controller
        self.tracker = None
        self.session_id = None
        self.timer.resetted.connect(self.handle_timer_reset)  # New slot
        self.timer.resetted.connect(lambda msg: create_textbox(msg))
  # Connected create_textbox function to the resetted signal

    def update_label(self):
        self.view.timer_label.setText(self.model.remaining_time.toString())

    @Slot()
    def toggle_timer(self):
        if self.timer.is_running:
            self.timer.pause()
            self.view.btn.setText('Start')
        else:
            start_time = datetime.now()
            ai_comment = "AI comment"
            self.session_id = self.db_controller.start_pomodoro_session(start_time)
            self.tracker = ActiveWindowTracker(self.db_controller, self.session_id)
            self.timer.session_id = self.session_id  # Add this line

            thread = threading.Thread(target=self.tracker.start_tracking)
            thread.start()

            atexit.register(self.tracker.stop_tracking)

            self.timer.start(self.tracker)  # Pass tracker to the timer
            self.view.btn.setText('Stop')

    @Slot()
    def update_timer(self):
        self.model.remaining_time = self.model.remaining_time.addSecs(-1)
        self.update_label()

        if self.model.remaining_time == QTime(0, 0):
            self.model.reset()


    def end_session(self, session_id):
        end_time = datetime.now()
        ai_comment = self.ai.generate_session_comment(session_id)
        self.db_controller.update_session_end_time_and_comment(session_id, end_time, ai_comment)

        # Show AI comment in a textbox
        create_textbox(ai_comment)



    @Slot()
    def handle_timer_reset(self):
        self.view.btn.setText('Start')
        self.end_session(self.session_id)  # Pass the session_id to the end_session method
