class PomodoroSession:
    def __init__(self, session_id, start_time, end_time, ai_comment):
        self.session_id = session_id
        self.start_time = start_time
        self.end_time = end_time
        self.ai_comment = ai_comment

class WindowActivity:
    def __init__(self, session_id, time, window_name):
        self.session_id = session_id
        self.time = time
        self.window_name = window_name
