import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from db2 import init_quotes_table, fetch_quote_from_api, get_user_theme
from streaks import StreakTracker

class QuoteAndStreakPanel(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.init_ui()
        self.load_user_theme()

    def init_ui(self):
        self.setWindowTitle("Motivational Quote Panel")
        self.setGeometry(300, 100, 600, 400)

        # Initialize quotes table
        result = init_quotes_table()
        if result is not True:
            print(f"Error initializing quotes table: {result}")
            sys.exit(1)

        # Create layout and set it
        layout = QVBoxLayout()

        # Add Heading (Quote of the Day)
        self.heading_label = QLabel("Quote of the Day")
        heading_font = QFont("Arial", 26, QFont.Bold)
        self.heading_label.setFont(heading_font)
        self.heading_label.setAlignment(Qt.AlignCenter)

        # Fetch/ retrieve cached quote
        quote, author = fetch_quote_from_api()

        # Create and set the quote text label
        self.quote_label = QLabel(quote)
        font = QFont("Arial", 20)
        font.setItalic(True)
        self.quote_label.setFont(font)
        self.quote_label.setAlignment(Qt.AlignCenter)
        self.quote_label.setWordWrap(True)  # Allow text wrapping for long quotes

        # Add widgets to the layout
        layout.addWidget(self.heading_label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.quote_label)
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.streak_tracker = StreakTracker(self.user_id)
        layout.addWidget(self.streak_tracker)
        # Set the layout to the window
        self.setLayout(layout)

    def refresh_theme(self):
        self.load_user_theme()
        self.streak_tracker.refresh_theme()

    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        if theme:
            self.apply_theme(theme)

    def apply_theme(self, theme):
        _, color_1, color_2, color_3, color_4 = theme.values()

        self.heading_label.setStyleSheet(f"""
            background-color: {color_4};
            color: {color_1};
        """)

        self.quote_label.setStyleSheet(f"""
            color: {color_2};
            background-color: {color_3};
            padding: 15px;
            border-radius: 8px;
        """)

        # Set background gradient and border for the panel itself
        base_style = f"""
            QWidget {{
                border: 2px solid {color_4};
                border-radius: 15px;
                padding: 20px;
            }}
        """
        self.setStyleSheet(base_style)