# timer_view.py
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel

class TimerView(QMainWindow):
    def __init__(self):
        
        super().__init__()
        

        # ウィンドウ設定
        self.setWindowTitle('Pomodoro Timer')
        self.setGeometry(100, 100, 300, 200)

        # タイマーラベル
        self.timer_label = QLabel(self)
        self.timer_label.setGeometry(20, 20, 260, 40)

        # スタート/ストップボタン
        self.btn = QPushButton('Start', self)
        self.btn.setGeometry(20, 80, 260, 40)
