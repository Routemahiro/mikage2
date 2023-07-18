# from models.timer import Timer
# # from models.task_list import TaskList
# from views.timer_view import TimerView


# class CharacterController:
#     def __init__(self):
#         self.view = TimerView(self)


# if __name__ == '__main__':
#     import sys
#     from PySide6.QtWidgets import QApplication

#     app = QApplication(sys.argv)

#     sys.exit(app.exec())

from models.timer import Timer
# from models.task_list import TaskList
from views.timer_view import TimerView
from controllers import ai_controller  # ここでai_controllerをインポート

class CharacterController:
    def __init__(self):
        self.timer = Timer()  # Timerインスタンスを作成
        self.view = TimerView(self)
        self.ai_instance = ai_controller.AIController()  # AIControllerインスタンスを作成

    def start_session(self):
        # Timerを開始
        self.timer.start()

    def end_session(self):
        # Timerを終了
        self.timer.stop()



if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    controller = CharacterController()
    sys.exit(app.exec())
