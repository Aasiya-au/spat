import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPalette, QColor
import sys
from db2 import get_all_users, get_user_theme

class Leaderboard(QWidget):
    def __init__(self, user_id):
        super().__init__()
    
        self.user_id = user_id
        # Layout
        layout = QVBoxLayout()

        # Create table widget
        self.tableWidget = QTableWidget()
        font = self.tableWidget.font()
        font.setPointSize(16)  # Increase font size
        self.tableWidget.setFont(font)
        self.tableWidget.setFixedSize(730, 550)  # Slightly smaller than window to fit padding
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)  # Increase row height
        self.tableWidget.verticalHeader().setVisible(False)  # Hide row numbers
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header_font = self.tableWidget.horizontalHeader().font()
        header_font.setPointSize(18)  # Set larger font size for headers
        self.tableWidget.horizontalHeader().setFont(header_font)
        self.tableWidget.setAlternatingRowColors(True)  # Enable alternating row colors

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
        self.tableWidget.resizeColumnsToContents()  # Adjust column widths based on content
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # Expand last column

        self.load_user_theme()
        # Load data into the table
        self.load_users()

    def load_user_theme(self):
        
        theme = get_user_theme(self.user_id)
        if theme:
            self.current_theme = theme
            self.apply_theme(theme)
        
    def apply_theme(self, theme):
        _, color_1, color_2, color_3, color_4 = theme.values()

        # Apply Background Color
        self.setStyleSheet(f"background-color: {color_2};")

        self.tableWidget.setStyleSheet(f"""
            QTableWidget {{
                background-color: {color_2};
                color: {color_1};
                alternate-background-color: {color_3};
                selection-background-color: {color_4};
                gridline-color: {color_1};
                border: 2px solid {color_1};
            }}
            QHeaderView::section {{
                background-color: {color_4};
                color: white;
                padding: 5px;
                border: 1px solid {color_1};
                font-weight: bold;
            }}
        """)

    def load_users(self):
        users = get_all_users()  # Fetch users from DB

        if users:
            column_names = list(users[0].keys())  # Get column names from dictionary keys
            self.tableWidget.setRowCount(len(users))
            self.tableWidget.setColumnCount(len(column_names))

            # Set table headers
            self.tableWidget.setHorizontalHeaderLabels(["Rank", "Username", "Total Study Points"])

            # Populate table
            for row_idx, user in enumerate(users):
                self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(str(user["rank"])))  # Insert rank
                for col_idx, col_name in enumerate(column_names):
                    self.tableWidget.setItem(row_idx, col_idx + 1, QTableWidgetItem(str(user[col_name])))
        else:
            print("No users found in the database.")

    def refresh_theme(self):
        self.load_user_theme()