import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import sys
from db2 import get_user_chat, get_user_theme

class ChatHistory(QWidget):
    def __init__(self, user_id):
        super().__init__()
    
        self.user_id = user_id
        self.resize(800, 600)  # Set a reasonable window size
        # Layout
        layout = QVBoxLayout()

        # Create table widget
        self.tableWidget = QTableWidget()
        font = self.tableWidget.font()
        font.setPointSize(14)  # Increase font size
        self.tableWidget.setFont(font)
        
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

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
        self.load_user_history()

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

    def load_user_history(self):
        users = get_user_chat(self.user_id)

        if users:
            column_names = list(users[0].keys())  # Get column names from dictionary keys
            self.tableWidget.setRowCount(len(users))
            self.tableWidget.setColumnCount(len(column_names))

            # Set table headers
            self.tableWidget.setHorizontalHeaderLabels(["User Query", "AI Response"])

            # Populate table
            for row_idx, user in enumerate(users):
                for col_idx, col_name in enumerate(column_names):
                    item = QTableWidgetItem(str(user[col_name]))
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                    item.setToolTip(str(user[col_name]))  # Optional: show full text on hover
                    self.tableWidget.setItem(row_idx, col_idx, item)
                    
            # Automatically resize rows and columns to fit contents
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
        else:
            print("No users found in the database.")

    def refresh_theme(self):
        self.load_user_theme()