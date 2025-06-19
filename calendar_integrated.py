import sys
import mysql.connector
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QLabel, QListWidget, QListWidgetItem, QApplication
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor,QFont
from db2 import get_user_theme

class StudyPlanner(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Study Calendar")
        self.setGeometry(100, 100, 800, 600)
        self.user_id = user_id
        self.init_ui()
        self.load_user_theme()

    def refresh_theme(self):
        self.load_user_theme()
        
    def apply_global_calendar_format(self):
        # Set format for all days (blackout default red/blue)
        format = QTextCharFormat()
        format.setForeground(QBrush(QColor(self.color_2)))  # Use your theme's primary text color
        format.setBackground(QBrush(QColor(self.color_3)))  # Optional: change background for all

        # Apply this format to all dates visible in the calendar
        today = QDate.currentDate()
        year = today.year()
        for month in range(1, 13):
            for day in range(1, 32):  # Max possible days in a month
                try:
                    qdate = QDate(year, month, day)
                    if qdate.isValid():
                        self.calendar.setDateTextFormat(qdate, format)
                except Exception:
                    continue

    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        if theme:
            self.apply_theme(theme)
    
    def apply_theme(self, theme):
        theme_id, self.color_1, self.color_2, self.color_3, self.color_4 = theme.values()
        self.apply_global_calendar_format()

        self.setStyleSheet(f"""
            QWidget {{ background-color: {self.color_3}; font-size: 14px; }}
            QLabel {{ color: {self.color_3}; font-weight: bold; font-size: 16px; }}
            QCalendarWidget QWidget {{ background-color: {self.color_2}; }}
            QCalendarWidget QToolButton {{ background-color: {self.color_1}; color: {self.color_4}; }}
            QCalendarWidget QTableView {{ selection-background-color: {self.color_1}; }}
            QListWidget {{ background-color: {self.color_4}; color: {self.color_1}; }}
        """)

    def init_ui(self):
        self.task_map = {}  # Maps datetime.date -> list of strings
        self.study_dates = set()

        # Layout setup
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.update_task_list)
        self.layout.addWidget(self.calendar)

        # Label for task list
        self.task_list_label = QLabel("Tasks Due:")
        self.layout.addWidget(self.task_list_label)

        # List widget to show tasks
        self.task_list_widget = QListWidget()
        self.layout.addWidget(self.task_list_widget)

    def set_task_data(self, task_data_list):
        """
        task_data_list: List of (datetime.date, str, bool) 
        Example: [(2025-05-04), "Finish math homework".True)]
        """
        for date, task_title, is_completed in task_data_list:
            self.study_dates.add(date)
            if date not in self.task_map:
                self.task_map[date] = []
            self.task_map[date].append((task_title, is_completed))

        self.highlight_due_dates()

    def highlight_due_dates(self):
        # Highlight all due task days on the calendar
        self.format = QTextCharFormat()
        self.format.setBackground(QBrush(QColor(f"{self.color_4}")))  # Light green
        for date in self.study_dates:
            qdate = QDate(date.year, date.month, date.day)
            self.calendar.setDateTextFormat(qdate, self.format)

    def update_task_list(self, qdate):
        pydate = qdate.toPyDate()
        self.task_list_widget.clear()

        tasks = self.task_map.get(pydate, [])
        for task_title, is_completed in tasks:
            item = QListWidgetItem(task_title)
            if is_completed:
                font = QFont()
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(QColor(f"{self.color_3}"))
            else:
                item.setForeground(QColor(f"{self.color_2}"))
            self.task_list_widget.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyPlanner(5)
    window.show()
    sys.exit(app.exec_())
