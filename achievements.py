import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea
from db2 import get_achievements, add_user_achievement, get_user_theme

class Achievements(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.init_ui()
        self.load_user_theme()
        self.load_achievements()
    
    def init_ui(self):
        self.main_layout = QVBoxLayout()
        
        # Achievement content area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)
    
    def load_user_theme(self):
        """Load the user's current theme"""
        theme = get_user_theme(self.user_id)
        if theme:
            self.current_theme = theme
            self.apply_theme(theme)
    
    def apply_theme(self, theme):
        """Apply theme colors to the UI components"""
        _, color_1, color_2, color_3, color_4 = theme.values()
        
        # Map the 4-color scheme to UI components
        self.setStyleSheet(f"background-color: {color_1};")
        self.scroll_content.setStyleSheet(f"background-color: {color_2}; border-radius: 10px;")
    
    def load_achievements(self):
        achievements = get_achievements(self.user_id)
        add_user_achievement(self.user_id)
        
        if achievements:
            for achievement in achievements:
                self.create_achievement_card(achievement["name"], achievement["description"])
    
    def reload_achievements(self):
        """Clear and reload achievement cards with current theme"""
        # Clear existing achievement cards
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Reload achievements with the current theme
        self.load_achievements()
    
    def refresh_theme(self):
        """Public method to refresh the theme and rebuild achievement cards"""
        self.load_user_theme()
        self.reload_achievements()
    
    def create_achievement_card(self, name, description):
        card = QFrame()
        
        theme_id, color_1, color_2, color_3, color_4 = self.current_theme.values()
        
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color_3};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        
        card.setFixedHeight(150)
        card.setFixedWidth(700)
        card_layout = QVBoxLayout()
        card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        name_label = QLabel(name)
        name_label.setStyleSheet(f"font-weight: bold; font-size: 20px; color: {color_1};")
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"font-size: 18px; color: {color_4};")
        desc_label.setWordWrap(True)
        
        card_layout.addWidget(name_label)
        card_layout.addWidget(desc_label)
        card.setLayout(card_layout)
        
        self.scroll_layout.addWidget(card)