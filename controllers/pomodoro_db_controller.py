#pomodoro_db_controller.py
import sqlite3
from models.pomodoro_models import PomodoroSession, WindowActivity
import os
from database.init_db import init_db

class PomodoroDBController:

    def __init__(self, db_path):
        self.db_path = db_path
        # データベースが存在しない場合にのみデータベース (およびテーブル) を作成する
        if not os.path.isfile(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            init_db()  # ここでテーブルを作成します

    def init_db(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PomodoroSession (
                session_id INTEGER PRIMARY KEY,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                ai_comment TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS WindowActivity (
                session_id INTEGER,
                time DATETIME NOT NULL,
                window_name TEXT NOT NULL,
                FOREIGN KEY(session_id) REFERENCES PomodoroSession(session_id)
            )
        ''')

        connection.commit()
        connection.close()

    def add_pomodoro_session(self, start_time, end_time, ai_comment):
        session = PomodoroSession(start_time, end_time, ai_comment)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PomodoroSession (start_time, end_time, ai_comment)
            VALUES (?, ?, ?)
            """, (session.start_time, session.end_time, session.ai_comment))
        conn.commit()
        session.id = cursor.lastrowid
        conn.close()
        return session.id

    def get_pomodoro_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM PomodoroSession WHERE session_id = ?
            """, (session_id,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return PomodoroSession(*row)

    def add_window_activity(self, session_id, time, window_name):
        activity = WindowActivity(session_id, time, window_name)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO window_activities (session_id, time, window_name)
            VALUES (?, ?, ?)
            """, (activity.session_id, activity.time, activity.window_name))
        conn.commit()
        activity.id = cursor.lastrowid
        conn.close()
        return activity.id
    
    def update_session_end_time_and_comment(self, session_id, end_time, ai_comment):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE PomodoroSession
            SET end_time = ?, ai_comment = ?
            WHERE session_id = ?
            """, (end_time, ai_comment, session_id))
        conn.commit()
        conn.close()

    def add_window_activity(self, session_id, timestamp, title):
        with sqlite3.connect(self.db_path) as conn:  # Create a temporary connection
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO WindowActivity (session_id, time, window_name)
                VALUES (?, ?, ?)
            ''', (session_id, timestamp, title,))
            conn.commit()


    def start_pomodoro_session(self, start_time):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PomodoroSession (start_time)
            VALUES (?)
            """, (start_time,))
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()
        return session_id

    def end_pomodoro_session(self, session_id, end_time, ai_comment):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE PomodoroSession
            SET end_time = ?, ai_comment = ?
            WHERE session_id = ?
            """, (end_time, ai_comment, session_id))
        conn.commit()
        conn.close()