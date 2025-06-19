import mysql.connector
from datetime import datetime
from db2 import start_study_session, end_study_session, get_user_theme
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLCDNumber, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime
import sys

class TimerUI(QWidget):
    def __init__(self, user):
        super().__init__() 
        self.user = user
        self.user_id = self.user["id"]
        self.initUI()
        self.start_time = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = QTime(0, 0, 0)
        self.load_user_theme()

    def initUI(self):
        self.setWindowTitle('Study Session Timer')
        self.setGeometry(100, 100, 1000, 500)
        self.layout = QVBoxLayout()

        self.timer_display = QLCDNumber(self)
        self.timer_display.setDigitCount(8)
        self.timer_display.display("00:00:00")
        self.layout.addWidget(self.timer_display)

        self.start_button = QPushButton('Start Session', self)
        self.start_button.clicked.connect(self.start_session)

        self.layout.addWidget(self.start_button)

        self.end_button = QPushButton('End Session', self)
        self.end_button.clicked.connect(self.end_session)

        self.end_button.setVisible(False)
        self.layout.addWidget(self.end_button)

        self.reset_button = QPushButton('Reset Timer', self)
        self.reset_button.clicked.connect(self.reset_timer)

        self.reset_button.setVisible(False)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        if theme:
            self.apply_theme(theme)

    def apply_theme(self, theme):
        _, color_1, color_2, color_3, color_4 = theme.values()
        self.setStyleSheet(f"background-color: {color_2};")  # Set background color

        self.timer_display.setStyleSheet(f"""
            QLCDNumber {{
                background-color: {color_3};
                color: {color_1};
                border: 2px solid {color_1};
                font-size: 24px;
            }}
        """)

        self.start_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_4};
                color: white;
                border: 2px solid {color_1};
                font-size: 18px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {color_1};
            }}
        """)

        self.end_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_4};
                color: white;
                border: 2px solid {color_1};
                font-size: 18px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {color_1};
            }}
        """)

        self.reset_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_4};
                color: white;
                border: 2px solid {color_1};
                font-size: 18px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {color_1};
            }}
        """)

    def refresh_theme(self):
        self.load_user_theme()

    def start_session(self):
        self.start_time = datetime.now()
        self.timer.start(1000)
        self.started_study_session = start_study_session(user_id=self.user["id"], start_time=datetime.now().strftime("%H:%M:%S"), session_date=datetime.now().date())
        self.start_button.setVisible(False)
        self.end_button.setVisible(True)
        self.reset_button.setVisible(False)

    def update_timer(self):
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.timer_display.display(self.elapsed_time.toString("hh:mm:ss"))

    def end_session(self):
        self.timer.stop()
        end_time = datetime.now()
        session_duration = end_time - self.start_time

        # Convert duration to string representation for database
        duration_str = str(session_duration)
        duration_minutes = session_duration.seconds / 60

        study_session = end_study_session(
            started_session=self.started_study_session,
            end_time=end_time.strftime("%H:%M:%S"),
            duration=duration_str,
            duration_in_min=duration_minutes
        )

        self.start_button.setVisible(False)
        self.end_button.setVisible(False)
        self.reset_button.setVisible(True)
        return study_session

    def reset_timer(self):
        self.timer_display.display("00:00:00")
        self.elapsed_time = QTime(0, 0, 0)
        self.start_button.setVisible(True)
        self.end_button.setVisible(False)
        self.reset_button.setVisible(False)