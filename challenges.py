import sys
import mysql.connector
from datetime import datetime, timedelta, date, time
from PyQt5.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton
from PyQt5.QtCore import Qt
from db2 import get_user_theme, get_daily_challenges, mark_challenge_completed, add_study_points, is_challenge_completed

class DailyChallenges(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.load_user_theme()
        self.init_ui()
        self.load_challenges()
        self.apply_theme()
    
    def init_ui(self):
        self.setWindowTitle("Daily Challenge")
        self.setGeometry(300, 100, 800, 600)

        self.main_layout = QVBoxLayout()
        
        # Challenges content area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        _, self.color_1, self.color_2, self.color_3, self.color_4 = theme.values()

    def apply_theme(self):
        # Set a simple background color for the window and scroll content
        self.setStyleSheet(f"background-color: {self.color_3}")  # Beige background
        self.scroll_content.setStyleSheet(f"background-color: {self.color_2}; border-radius: 10px;")  # Pink scroll content
    
        # Hardcoded colors for the card
        self.card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color_1};
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }}
        """)  # Teal background for the card
        self.name_difficulty_label.setStyleSheet(f"font-weight: bold; font-size: 24px; color: {self.color_3};")
        self.desc_label.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {self.color_4};")
        self.points_label.setStyleSheet(f"font-size: 20px; font-style: italic; font-weight: bold; color: {self.color_4};")
        self.done_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color_2};
                color: {self.color_1};
                border-radius: 5px;
                padding: 8px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color_2};
            }}
            QPushButton:disabled {{
                background-color: grey;
                color: white;
            }}
        """)  # Beige button, teal text, pink hover

    def refresh_theme(self):
        self.load_user_theme()
        self.apply_theme()
        
    def load_challenges(self):
        challenges = get_daily_challenges()
        
        if challenges:
            # Since we expect only one challenge per day
            challenge = challenges[0]
            self.create_challenge_card(
                challenge["challenge_id"],
                challenge["name"],
                challenge["description"],
                challenge["difficulty"],
                challenge["points"]
            )
        else:
            # Fallback message if no challenge is available
            self.no_challenge_label = QLabel("No challenge available today.")
            self.no_challenge_label.setStyleSheet("font-size: 20px; color: black")  # Black text for visibility
            self.no_challenge_label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(self.no_challenge_label)
            self.scroll_content.adjustSize()  # Force the scroll content to adjust its size
            self.scroll_area.adjustSize()  # Force the scroll area to adjust its size
    
    def reload_challenges(self):
        """Clear and reload challenge cards"""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.load_challenges()
    
    def create_challenge_card(self, challenge_id, name, description, difficulty, points):
        self.card = QFrame()
        
        self.card.setFixedWidth(700)
        self.card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        
        # Main layout for the card
        card_layout = QVBoxLayout()
        
        # Challenge name and difficulty
        self.name_difficulty_label = QLabel(f"{name} ({difficulty})")
        self.name_difficulty_label.setWordWrap(True)
        
        # Description
        self.desc_label = QLabel(description)
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignLeft)
        
        # Points
        self.points_label = QLabel(f"Points: {points}")
        self.points_label.setWordWrap(True)
        
        # Done button
        self.done_button = QPushButton("Done")
        self.done_button.setFixedSize(100, 40)

        # Disable button if challenge is already completed
        if is_challenge_completed(self.user_id, challenge_id):  # Updated to use db2 function
            self.done_button.setEnabled(False)
            self.done_button.setText("Completed")
        else:
            self.done_button.clicked.connect(lambda: self.complete_challenge(challenge_id, points, self.done_button))
        
        # Layout for points and button
        points_button_layout = QHBoxLayout()
        points_button_layout.addWidget(self.points_label)
        points_button_layout.addStretch()
        points_button_layout.addWidget(self.done_button)
        
        card_layout.addWidget(self.name_difficulty_label)
        card_layout.addWidget(self.desc_label)
        card_layout.addLayout(points_button_layout)
        self.card.setLayout(card_layout)
        
        self.scroll_layout.addWidget(self.card)
    
    def complete_challenge(self, challenge_id, points, button):
        """Mark the challenge as completed and add points to the user"""
        today = date.today()
        result = mark_challenge_completed(self.user_id, challenge_id, today)
        if result is True:
            # Add points to the user
            add_study_points(self.user_id, points)
            # Disable the button to prevent duplicate submissions
            button.setEnabled(False)
            button.setText("Completed")
        else:
            print(f"Failed to mark challenge as completed: {result}")