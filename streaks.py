import sys
import mysql.connector
from datetime import date, timedelta
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QCalendarWidget
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor
from db2 import log_user_login, get_login_streak, get_login_dates_for_month, get_user_theme

class MonthlyStreakView(QDialog):
    def __init__(self, user_id, theme):
        super().__init__()
        self.user_id = user_id
        self.theme = theme
        self.setWindowTitle("Monthly Login Streaks")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # Remove vertical header (row numbers)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.LongDayNames)  # Show full day names (Sun-Sat)
        self.calendar.currentPageChanged.connect(self.highlight_login_days)
        layout.addWidget(self.calendar)
        self.setLayout(layout)
        self.apply_theme(self.theme)
        self.highlight_login_days()

    def apply_theme(self, theme):
        _, color_1, color_2, color_3, color_4 = theme.values()

        self.calendar.setStyleSheet(f"""
            QCalendarWidget {{
                background-color: {color_2};
                border: 1px solid {color_1};
                border-radius: 5px;
            }}
            QCalendarWidget QTableView {{
                background-color: {color_4};
                gridline-color: {color_3};
            }}
            QCalendarWidget QTableView::item {{
                padding: 5px;
                border: 1px solid {color_3};
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                color: {color_1};
            }}
            /* Navigation bar (entire header area including month/year and buttons) */
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background-color: {color_3};
            }}
            /* Navigation buttons (previous/next month) */
            QCalendarWidget QWidget#qt_calendar_prevmonth,
            QCalendarWidget QWidget#qt_calendar_nextmonth {{
                background-color: {color_1};
                color: {color_2};
                border: none;
                border-radius: 5px;
                width: 20px;
                height: 20px;
            }}
            QCalendarWidget QWidget#qt_calendar_prevmonth:hover,
            QCalendarWidget QWidget#qt_calendar_nextmonth:hover {{
                background-color: {color_1};
            }}
            /* Month/year header button */
            QCalendarWidget QToolButton {{
                background-color: {color_2}; /* Soft pink */
                color: {color_1};
                border: none;
                border-radius: 5px;
                padding: 2px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: {color_3};
            }}
            QCalendarWidget QMenu {{
                background-color: {color_2};
                color: {color_3};
            }}
        """)

    def highlight_login_days(self):
        year = self.calendar.yearShown()
        month = self.calendar.monthShown()
        login_dates = get_login_dates_for_month(self.user_id, year, month)
        self.format = QTextCharFormat()
        self.format.setBackground(QBrush(QColor("#FFD700")))  # Gold for login days
        for login_date in login_dates:
            qdate = QDate(login_date.year, login_date.month, login_date.day)
            self.calendar.setDateTextFormat(qdate, self.format)

class StreakTracker(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        log_user_login(self.user_id)
        self.init_ui()
        self.load_user_theme()
        self.update_streak()

    def refresh_theme(self):
        self.load_user_theme()

    def load_user_theme(self):
        self.theme = get_user_theme(self.user_id)
        self.apply_theme(self.theme)

    def apply_theme(self, theme):
        _, color_1, color_2, color_3, color_4 = theme.values()
        self.title_label.setStyleSheet(f"color: {color_4}; font-weight: bold; font-size: 18px;")
        self.streak_label.setStyleSheet(f"color: {color_4}; font-weight: bold; font-size: 24px;")
        self.view_all_button.setStyleSheet(f"background-color: {color_3}; color: {color_1}; padding: 5px; border-radius: 5px;")

    def init_ui(self):
        self.setWindowTitle("Streak Tracker")
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("Login Streak Tracker")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Streak label
        self.streak_label = QLabel("Streak: 0 days")
        self.streak_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.streak_label)

        # Last 7 days login indicators
        self.day_indicators_layout = QHBoxLayout()
        self.day_indicators_layout.setSpacing(10)
        self.day_indicators = []
        for _ in range(7):
            day_label = QLabel()
            day_label.setFixedSize(30, 30)
            day_label.setAlignment(Qt.AlignCenter)
            self.day_indicators_layout.addWidget(day_label)
            self.day_indicators.append(day_label)
        layout.addLayout(self.day_indicators_layout)

        # View All Streaks button
        self.view_all_button = QPushButton("View All Streaks")
        self.view_all_button.clicked.connect(self.open_monthly_view)
        layout.addWidget(self.view_all_button)

        self.setLayout(layout)

    def update_streak(self):
        streak, login_dates = get_login_streak(self.user_id)
        self.streak_label.setText(f"Streak: {streak} days")

        today = date.today()
        for i in range(7):
            day = today - timedelta(days=i)
            label = self.day_indicators[i]
            if day in login_dates:
                label.setText("✔")
                label.setStyleSheet("color: green; font-size: 20px;")
            else:
                label.setText("✘")
                label.setStyleSheet("color: red; font-size: 20px;")

    def open_monthly_view(self):
        monthly_view = MonthlyStreakView(self.user_id, self.theme)
        monthly_view.exec_()