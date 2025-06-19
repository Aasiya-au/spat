import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from db2 import get_user, get_user_theme

class Profile(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        
        # Verify user exists before proceeding
        user = get_user(self.username)
        if user:
            self.user_id = user['id']
        else:
            print(f"Warning: User {username} does not exist in the database.")
            self.user_id = None
        
        self.init_ui()
        self.load_user_theme()
        self.load_profile_data()
    
    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
    
    def load_user_theme(self):
        if self.user_id:
            theme = get_user_theme(self.user_id)
            if theme:
                self.apply_theme(theme)
    
    def apply_theme(self, theme):
        """Apply theme colors to the UI components"""
        _, color_1, color_2, color_3, color_4 = theme.values()
        
        # Map the 4-color scheme to UI components
        self.setStyleSheet(f"""
            QWidget {{
                font-size: 14px;
            }}
            QLabel {{
                font-weight: bold;
                padding: 5px;
                color: {color_2};
                font-size: 16px;
            }}
        """)
    
    def load_profile_data(self):
        """Load user profile data and create labels"""
        # Clear existing widgets
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        print("Getting user data")
        user = get_user(self.username)
        
        if user:
            print("User found, creating labels")
            self.main_layout.addWidget(self.create_label(f"User ID: {user['id']}"))
            self.main_layout.addWidget(self.create_label(f"Username: {user['username']}"))
            self.main_layout.addWidget(self.create_label(f"Email: {user['email']}"))
            self.main_layout.addWidget(self.create_label(f"Study Points: {user['total_study_points']}"))
            self.main_layout.addWidget(self.create_label(f"Tasks Completed: {user['total_tasks_completed']}"))
            self.main_layout.addWidget(self.create_label(f"Topics Completed: {user['total_topics_completed']}"))
        else:
            print("User not found, creating label")
            self.main_layout.addWidget(self.create_label("User not found or error occurred"))
    
    def create_label(self, text):
        label = QLabel(text)
        return label
    
    def refresh_theme(self):
        """Public method to refresh the theme and rebuild profile data"""
        self.load_user_theme()
        self.load_profile_data()