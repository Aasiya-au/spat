import sys
import os
import mysql.connector
from functools import partial
from PyQt5.QtWidgets import (QApplication, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from db2 import get_all_themes, get_user_theme, set_user_theme, get_all_characters, get_user_character, set_user_character

# Set working directory to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ThemeWidget(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.selected_character_id = None
        
        self.themes = get_all_themes()
        self.characters = get_all_characters()
        
        self.init_ui()
        self.load_user_preferences()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.content_area = QWidget()
        content_layout = QVBoxLayout(self.content_area)

        self.header_label = QLabel("Appearance")
        self.header_label.setAlignment(Qt.AlignCenter)
        
        self.info_label = QLabel("Your text will look like this.")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.pic_label = QLabel()
        self.pic_label.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(self.header_label)
        content_layout.addWidget(self.info_label)
        content_layout.addWidget(self.pic_label)
        content_layout.addStretch()

        self.theme_buttons = QWidget()
        theme_layout = QHBoxLayout(self.theme_buttons)
        
        self.character_buttons = QWidget()
        character_layout = QHBoxLayout(self.character_buttons)

        self.theme_button_list = []
        for theme in self.themes:
            theme_id = theme["id"]
            button = QPushButton(f"Theme {theme_id}")
            # Use partial instead of lambda to avoid closure issues
            button.clicked.connect(partial(self.change_theme, theme_id))
            theme_layout.addWidget(button)
            self.theme_button_list.append(button)

        self.character_button_list = []
        for character in self.characters:
            character_id = character["id"]
            button = QPushButton(f"Character {character_id}")
            button.clicked.connect(partial(self.change_character, character_id))
            character_layout.addWidget(button)
            self.character_button_list.append(button)

        main_layout.addWidget(self.content_area)
        main_layout.addWidget(self.theme_buttons)
        main_layout.addWidget(self.character_buttons)

    def load_user_preferences(self):
        """Load both theme and character preferences in one method"""
        theme = get_user_theme(self.user_id)
        if theme:
            self.apply_theme(theme)

        character = get_user_character(self.user_id)
        if character:
            self.selected_character_id = character["id"]
            self.apply_character(character)
            self.update_image(character["name"])

    def update_image(self, character_name):
        image_path = f"{character_name}.png"
        
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            self.pic_label.clear()
            return
            
        pic = QPixmap(image_path)
        if pic.isNull():
            print(f"Failed to load image: {image_path}")
            self.pic_label.clear()
        else:
            scaled_pic = pic.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.pic_label.setPixmap(scaled_pic)
            self.pic_label.resize(scaled_pic.width(), scaled_pic.height())

    def change_theme(self, theme_id):
        theme = next((t for t in self.themes if t["id"] == theme_id), None)

        if theme:
            self.apply_theme(theme)
            if not set_user_theme(self.user_id, theme_id):
                print(f"Failed to set theme {theme_id} for user {self.user_id}")

    def change_character(self, character_id):
        character = next((c for c in self.characters if c["id"] == character_id), None)
        
        if character:
            self.selected_character_id = character_id
            self.apply_character(character)
            if not set_user_character(self.user_id, character_id):
                print(f"Failed to set character {character_id} for user {self.user_id}")
            self.update_image(character["name"])

    def create_button_style(self, is_selected=False):
        if is_selected:
            return f"""
                QPushButton {{
                    background-color: {self.color_4};
                    color: {self.color_1};
                    border: 2px solid {self.color_3};
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: {self.color_3};
                    color: {self.color_1};
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: {self.color_4};
                }}
            """

    def apply_character(self, character=None):
        if character is not None:
            self.selected_character_id = character["id"]
        
        # Reset all button styles
        for button in self.character_button_list:
            button.setStyleSheet(self.create_button_style(False))
        
        # Highlight selected button
        if self.selected_character_id is not None:
            button_idx = int(self.selected_character_id) - 1
            if 0 <= button_idx < len(self.character_button_list):
                self.character_button_list[button_idx].setStyleSheet(self.create_button_style(True))

    def apply_theme(self, theme):
        # Extract theme colors
        theme_id = theme["id"]
        self.color_1 = theme["color_1"]
        self.color_2 = theme["color_2"]
        self.color_3 = theme["color_3"]
        self.color_4 = theme["color_4"]
        
        # Apply styles
        self.setStyleSheet(f"background-color: {self.color_1};")
        self.header_label.setStyleSheet(f"color: {self.color_3}; font-size: 24px; font-weight: bold;")
        self.content_area.setStyleSheet(f"background-color: {self.color_2}; border-radius: 10px;")
        self.info_label.setStyleSheet(f"color: {self.color_4}; font-size: 18px;")
        
        # Reset all theme buttons
        for button in self.theme_button_list:
            button.setStyleSheet(self.create_button_style(False))
            
        # Highlight selected theme button
        button_idx = int(theme_id) - 1
        if 0 <= button_idx < len(self.theme_button_list):
            self.theme_button_list[button_idx].setStyleSheet(self.create_button_style(True))

        if self.selected_character_id is not None:
            self.apply_character()