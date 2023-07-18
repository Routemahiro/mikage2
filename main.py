import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication
from controllers.timer_controller import TimerController
from controllers.character_controller import CharacterController
from controllers.ai_controller import AIController
from controllers.ActiveWindowTracker import ActiveWindowTracker
from controllers.pomodoro_db_controller import PomodoroDBController
# from database.init_db import start_pomodoro_session, end_pomodoro_session
import time
import threading

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # timer_controller = TimerController()
    
    db_controller = PomodoroDBController('database/data/mikage_timer.db')
    ai_controller = AIController()    
    character_controller = CharacterController()
    timer_controller = TimerController(db_controller, ai_controller)
    
    timer_controller.view.show()

    # ディスプレイサイズを取得します
    screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    


    sys.exit(app.exec())