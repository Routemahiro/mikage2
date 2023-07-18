from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QIcon, QPalette, QColor
from PySide6.QtCore import Qt, QPoint, QSize
from controllers import ai_controller
from PySide6.QtWidgets import QVBoxLayout

class CharacterWindow(QWidget):
    def __init__(self, pomodoro_controller):
        super().__init__()
        self.pomodoro_controller = pomodoro_controller

        # キャラクター画像
        self.character_label = QLabel(self)
        pixmap = QPixmap("img\character.png")

        # ディスプレイサイズの取得
        screen = QApplication.primaryScreen().availableGeometry()

        # 画像をディスプレイサイズの3分の1にリサイズ
        resize_bairitsu = 2.5
        pixmap = pixmap.scaled(screen.width() // resize_bairitsu, screen.height() // resize_bairitsu, Qt.KeepAspectRatio)

        self.character_label.setPixmap(pixmap)
        self.character_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        # 設定ボタン
        self.setting_button = QPushButton(self)
        self.setting_button.setIcon(QIcon('img\setting_icon.png'))  # アイコンを設定
        self.setting_button.setIconSize(QSize(40, 40))  # アイコンサイズを設定
        self.setting_button.setFixedSize(QSize(50, 50))  # ボタンのサイズを設定
        
        # ボタンの背景を透明にするためのスタイルシートを設定
        self.setting_button.setStyleSheet("background-image: url('img\transparent_background.png'); border: none;")

        self.setting_button.setAttribute(Qt.WA_TranslucentBackground)

        # ボタンの位置を移動
        button_pos_x = 240  # これは任意のx座標
        button_pos_y = self.character_label.height() // 15  
        self.setting_button.move(button_pos_x, button_pos_y)  # (x, y)座標を指定

        # テキストエディットエリア
        self.chat_text_area = QTextEdit()
        
        palette = self.chat_text_area.palette()
        palette.setColor(QPalette.Base, QColor(0, 0, 0, 127))  # 背景色を半透明の黒に
        palette.setColor(QPalette.Text, QColor(255, 255, 255))  # テキスト色を白に
        self.chat_text_area.setPalette(palette)

        self.chat_text_area.textChanged.connect(self.adjust_text_area_height)

        self.chat_text_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 125);
                border-radius: 10px;
                padding: 1px;
                color: white;
            }
        """)




        # 初期は2行分の高さに設定
        self.chat_text_area.setMaximumHeight(self.chat_text_area.fontMetrics().lineSpacing() * 1)

        # ウィンドウ設定
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ボタンの背景を透明に
        self.setting_button.setAttribute(Qt.WA_TranslucentBackground)

        # ドラッグでウィンドウを移動するための変数
        self.m_drag = False
        self.m_DragPosition = QPoint()

        # 送信ボタンの作成
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)

        # レイアウトの設定
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.character_label)
        self.layout.addWidget(self.chat_text_area)
        self.layout.addWidget(self.send_button)  # 送信ボタンをレイアウトに追加

        self.setLayout(self.layout)
        # テキストエリアにフォーカスを設定
        self.chat_text_area.setFocus()        



        
    def send_message(self):
            # AIコントローラのインスタンス化
        ai_instance = ai_controller.AIController()
        user_message = self.chat_text_area.toPlainText()  # ユーザーが入力したテキストを取得
        self.chat_text_area.clear()  # テキストエディットエリアをクリア

        # ユーザーが何も入力していない場合は、何もしない
        if user_message.strip() == "":
            return

        # ユーザーのメッセージをAIに送信し、応答を取得
        character_response = self.pomodoro_controller.ai_instance.add_user_message(user_message)

        response_label = QLabel(f"user: {user_message}")
        response_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 127);
                border-radius: 10px;
                padding: 10px;
                color: white;
            }
        """)
        self.layout.addWidget(response_label)  # レイアウトに追加


        # 応答をテキストエディットエリアに表示
        response_label = QLabel(f"美影: {character_response}")
        response_label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 127);
                border-radius: 10px;
                padding: 10px;
                color: white;
            }
        """)
        self.layout.addWidget(response_label)  # レイアウトに追加



    def adjust_text_area_height(self):
        # テキストエリアの内容に基づいて高さを調整
        doc_height = self.chat_text_area.document().size().height()+10
        self.chat_text_area.setMaximumHeight(doc_height + 5)  # +5はパディング分
              

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    # マウスが移動した時のイベント
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    # マウスボタンが離された時のイベントsd
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = False




class TimerView(QWidget):
    def __init__(self, pomodoro_controller):
        super().__init__()

        # キャラクターウィンドウを作成し表示
        self.character_window = CharacterWindow(pomodoro_controller)
        self.character_window.show()

        # Layoutを設定
        self.layout = QVBoxLayout()  # 追加

        # タイマーのスタートボタンを押したときのアクションを設定
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(pomodoro_controller.start_session)
        self.layout.addWidget(self.start_button)
        
        # タイマーのリセットボタンを押したときのアクションを設定
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(pomodoro_controller.end_session)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

    def update_start_button_text(self, text):
        self.start_button.setText(text)

    def update_time_label(self, time_text):
        self.time_label.setText(time_text)

from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsPathItem
from PySide6.QtGui import QColor, QPainter, QPainterPath
from PySide6.QtCore import Qt, QRectF, QTimer

class CustomGraphicsView(QGraphicsView):
    def mousePressEvent(self, event):
        self.close()

def create_textbox(text):
    # Check if QApplication instance exists, create one if not
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # QGraphicsView & QGraphicsScene setup
    view = CustomGraphicsView()
    scene = QGraphicsScene()
    view.setScene(scene)
    view.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Remove window frame, set transparent background, and ensure window stays on top
    view.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    view.setStyleSheet("background: transparent")

    # Create text and set properties
    text_item = QGraphicsTextItem(text)
    text_item.setDefaultTextColor(QColor('white'))
    text_item.setTextWidth(380)  # Enable word wrap
    text_item.setZValue(1)  # Set the Z value to ensure it's above the rectangle

    # Get bounding rectangle of the text item
    text_rect = text_item.boundingRect()

    # Create rounded rectangle
    path = QPainterPath()
    padding = 20  # Padding around text
    path.addRoundedRect(QRectF(0, 0, text_rect.width() + 2*padding, text_rect.height() + 2*padding), 10, 10)  # Add rounded rectangle to the path

    rect = QGraphicsPathItem(path)
    rect.setBrush(QColor('black'))
    rect.setPen(QColor('black'))
    rect.setPos(200, 200)  # Set the position of the rectangle
    rect.setZValue(0)  # Set the Z value to ensure it's beneath the text

    text_item.setPos(210, 210)  # Set the position of the text

    # Add items to scene
    scene.addItem(rect)
    scene.addItem(text_item)

    # Set view to fit the scene's content
    view.fitInView(scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
    view.show()

    # Set timer to close window after 15 seconds
    QTimer.singleShot(15000, view.close)  # 15000 milliseconds = 15 seconds

    # Execute application
    # app.exec()




