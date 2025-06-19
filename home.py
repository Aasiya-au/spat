import sys
import os
import mysql.connector
from db2 import get_user_character, get_user_theme
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from quotes_final import QuoteAndStreakPanel
from challenges import DailyChallenges

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Home(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.init_ui()
        self.apply_theme()
        self.apply_character()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Create tabs
        self.tabs = QTabWidget()

        # Overview tab
        self.overview_tab = QWidget()
        self.overview_layout = QVBoxLayout()
        self.overview_tab.setLayout(self.overview_layout)

        self.text_label1 = QLabel("Welcome to the study planner! I'm your guide.")
        self.text_label1.setStyleSheet("background: transparent")
        self.text_label1.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel()

        self.text_label2 = QLabel("These are the panels on the left.")
        self.text_label2.setStyleSheet("background: transparent")
        self.text_label2.setAlignment(Qt.AlignCenter)

        self.overview_layout.addWidget(self.text_label1)
        self.overview_layout.addWidget(self.image_label)
        self.overview_layout.addWidget(self.text_label2)

        # Other tabs
        self.challenge_tab = DailyChallenges(self.user_id)
        self.quote_tab = QuoteAndStreakPanel(self.user_id)

        # Add tabs to tab widget
        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.challenge_tab, "Daily Challenge")
        self.tabs.addTab(self.quote_tab, "Quotes")

        # Add tab widget to main layout
        self.main_layout.addWidget(self.tabs)

    def apply_character(self):
        character = get_user_character(self.user_id)
        if character:
            _, character_name = character.values()
            pmap = QPixmap(f"{character_name}.png")
            if pmap.isNull():
                print("Failed to load character image")
            else:
                scaled_pic = pmap.scaled(200, 200)
                self.image_label.setPixmap(scaled_pic)
                self.image_label.setAlignment(Qt.AlignCenter)
                self.image_label.resize(pmap.width(), pmap.height())
        else:
            print("Error! No image found")

    def apply_theme(self):
        theme = get_user_theme(self.user_id)
        if theme:
            _, color_1, color_2, color_3, color_4 = theme.values()
            self.setStyleSheet(f"background-color: {color_1}")
            self.tabs.setStyleSheet(f"""
                QTabWidget::pane {{
                    border: none; /* removes white border around tabs */
                    background: {color_1};
                }}
                QTabBar::tab {{
                    background: {color_2};
                    color: {color_4};
                    font-size: 18px;
                    padding: 10px 20px;
                    min-width: 205px;       /* Increase tab button width */
                    min-height: 40px;        /* Increase tab button height */
                    border-radius: 10px;
                    margin: 2px;
                }}
                QTabBar::tab:selected {{
                    background: {color_3};
                    font-weight: bold;
                }}
            """)

            self.text_label1.setStyleSheet(f"font-size: 20px; color: {color_3}; font-weight: bold")
            self.text_label2.setStyleSheet(f"font-size: 18px; color: {color_2}")
        else:
            print("Error loading theme")

    def refresh_theme(self):
        self.apply_theme()
        self.apply_character()
        if hasattr(self.challenge_tab, 'refresh_theme'):
            self.challenge_tab.refresh_theme()
        if hasattr(self.quote_tab, 'refresh_theme'):
            self.quote_tab.refresh_theme()