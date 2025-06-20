import sys
import mysql.connector
import datetime
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QDialog, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont
import google.generativeai as ai
from db2 import log_api_call, load_user_chat, save_message, delete_history, get_user_chat, get_user_theme

class ApiThread(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, model, message):
        super().__init__()
        self.model = model
        self.message = message

    def run(self):
        try:
            response = self.model.generate_content(self.message)
            self.response_received.emit(response.text)
        except Exception as e:
            self.response_received.emit(f"Error: {str(e)}")

class HistoryDialog(QDialog):
    def __init__(self, parent=None, user_id=None, theme=None):
        super().__init__(parent)
        self.user_id = user_id
        self.theme = theme
        self.setWindowTitle("Chat History")
        self.setGeometry(200, 200, 800, 400)

        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        font = self.tableWidget.font()
        font.setPointSize(14)
        self.tableWidget.setFont(font)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header_font = self.tableWidget.horizontalHeader().font()
        header_font.setPointSize(18)
        self.tableWidget.horizontalHeader().setFont(header_font)
        self.tableWidget.setAlternatingRowColors(True)
        layout.addWidget(self.tableWidget)

        self.delete_button = QPushButton("Delete History")
        self.delete_button.clicked.connect(self.delete_history)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

        self.load_user_history()
        self.apply_theme(self.theme)

    def apply_theme(self, theme):
        _, color_1, color_2, color_3, color_4 = theme.values()
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
        self.delete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_3}; 
                color: {color_1}; 
                border: none; 
                padding: 12px; 
                border-radius: 6px; 
                font-size: 14px; 
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {color_2}; }}
            QPushButton:pressed {{ background-color: {color_4}; }}
        """)

    def load_user_history(self):
        users = get_user_chat(self.user_id)
        if users:
            column_names = list(users[0].keys())
            self.tableWidget.setRowCount(len(users))
            self.tableWidget.setColumnCount(len(column_names))
            self.tableWidget.setHorizontalHeaderLabels(["User Query", "AI Response"])
            for row_idx, user in enumerate(users):
                for col_idx, col_name in enumerate(column_names):
                    item = QTableWidgetItem(str(user[col_name]))
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                    item.setToolTip(str(user[col_name]))
                    self.tableWidget.setItem(row_idx, col_idx, item)
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
        else:
            print("No chat history found for this user.")

    def delete_history(self):
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete all chat history?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            error = delete_history(self.user_id)
            if error:
                QMessageBox.critical(self, "Error", error)
            else:
                self.tableWidget.setRowCount(0)
                QMessageBox.information(self, "Success", "Chat history has been deleted.")

class ChatBot(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.API_KEY = "YOUR_API_KEY"
        ai.configure(api_key=self.API_KEY)
        self.model = ai.GenerativeModel("gemini-2.0-flash")
        self.chat_messages = []  # Stores all chat messages
        self.theme = get_user_theme(self.user_id)
        self.initUI()
        self.load_user_chat()
        self.apply_theme(self.theme)

    def refresh_theme(self):
        self.theme = get_user_theme(self.user_id)
        self.apply_theme(self.theme)
        self.update_chat_display()

    def apply_theme(self, theme):
        _, color1, color2, color3, color4 = theme.values()

        self.chat_history.setStyleSheet(f"""
            background-color: {color1};
            border: 1px solid {color3};
            border-radius: 10px;
        """)

        self.setStyleSheet(f"""
            QWidget {{ background-color: {color2}; font-family: 'Segoe UI', Arial, sans-serif; }}
            QLineEdit {{
                background-color: #FFFFFF; color: #333333;
                border: 1px solid {color3}; padding: 12px;
                border-radius: 20px; font-size: 14px;
            }}
            QLineEdit:focus {{ border: 2px solid {color4}; }}
            QPushButton {{
                background-color: {color4}; color: #FFFFFF;
                border: none; padding: 12px;
                border-radius: 20px; font-size: 14px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {color3}; }}
            QPushButton:pressed {{ background-color: {color1}; }}
            QScrollBar:vertical {{
                border: none; background: {color2}; width: 10px;
                margin: 0px 0px 0px 0px; border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {color3}; min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

    def initUI(self):
        self.setWindowTitle("Study Planner with AI Chatbot")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask a study-related question...")
        self.send_button = QPushButton("Send")
        self.history_button = QPushButton("View History")
        input_layout.addWidget(self.input_field, 4)
        input_layout.addWidget(self.send_button, 1)
        input_layout.addWidget(self.history_button, 1)
        layout.addLayout(input_layout)

        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
        self.history_button.clicked.connect(self.show_history)

        self.setLayout(layout)

    def send_message(self):
        user_input = self.input_field.text().strip()
        if user_input:
            # Add user message and show "Thinking..." message
            self.chat_messages.append(("user", user_input))
            self.chat_messages.append(("thinking", "Thinking..."))  # Temporary placeholder

            # Update the chat display
            self.update_chat_display()

            self.input_field.clear()
            self.send_button.setEnabled(False)

            context = "You are a helpful tutor explaining study topics in a clear, very concise, and educational manner."
            full_message = context + "\n\nQuestion: " + user_input

            self.api_thread = ApiThread(self.model, full_message)
            self.api_thread.response_received.connect(lambda response: self.display_response(response, user_input))
            self.api_thread.start()

    def display_response(self, response, user_input):
        # Replace "Thinking..." with the AI response
        for i, (sender, message) in enumerate(self.chat_messages):
            if sender == "thinking":
                self.chat_messages[i] = ("ai", response)  # Replace with actual response
                break

        # Update the chat display
        self.update_chat_display()

        self.send_button.setEnabled(True)

        # Save the message to the database
        error = save_message(self.user_id, user_input, response)
        if error:
            self.chat_messages.append(("error", f"Error saving message: {error}"))
            self.update_chat_display()
            # Log the API call after saving the message
            # Get the current time for response time
        response_time = int(time.time() * 1000)  # Time in milliseconds

         # Log the API request details
        log_api_call(
            api_endpoint='/chatbot',  # API endpoint where the message is processed
            request_data=f"User query: {user_input}, AI response: {response}",
            response_status='success',  # You can track if it succeeded
            response_time=response_time,  # Log the response time
            user_id=self.user_id  # Log the user ID
        )

    def update_chat_display(self):
        if not hasattr(self, 'theme'):
            self.chat_history.setHtml("Theme not loaded.")
            return

        _, color1, color2, color3, color4 = self.theme.values()

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; }}
            .message-container {{ margin: 10px 0; }}
            .user-message {{ display: flex; justify-content: flex-end; }}
            .user-bubble {{
                max-width: 70%;
                background-color: {color4};
                color: white;
                padding: 10px 15px;
                border-radius: 18px 18px 0px 18px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            }}
            .ai-message {{ display: flex; justify-content: flex-start; }}
            .ai-bubble {{
                max-width: 70%;
                background-color: {color3};
                color: #333333;
                padding: 10px 15px;
                border-radius: 18px 18px 18px 0px;
                border-left: 3px solid {color4};
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }}
            .thinking {{
                margin: 5px 0;
                font-style: italic;
                color: {color4};
                text-align: center;
            }}
            .error {{
                max-width: 80%;
                background-color: #FFCDD2;
                color: #B71C1C;
                padding: 10px 15px;
                border-radius: 10px;
                border: 1px solid #E57373;
                margin: 10px auto;
            }}
        </style>
        </head>
        <body>
        """

        for sender, message in self.chat_messages:
            if sender == "user":
                html_content += f"""
                <div class="message-container user-message">
                    <div class="user-bubble">{message}</div>
                </div>
                """
            elif sender == "ai":
                html_content += f"""
                <div class="message-container ai-message">
                    <div class="ai-bubble">{message}</div>
                </div>
                """
            elif sender == "thinking":
                html_content += f"""<div class="thinking">{message}</div>"""
            elif sender == "error":
                html_content += f"""<div class="error"><b>Error:</b> {message}</div>"""

        html_content += "</body></html>"

        self.chat_history.setHtml(html_content)
        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def load_user_chat(self):
        rows = load_user_chat(self.user_id)
        self.chat_messages = []
        for row in rows:
            if row["user_query"] != "Initial greeting":  # Skip initial greetings
                if row["user_query"]:  # Add user message if it exists
                    self.chat_messages.append(("user", row["user_query"]))
                if row["ai_response"]:  # Add AI response if it exists
                    self.chat_messages.append(("ai", row["ai_response"]))
        self.update_chat_display()

    def show_history(self):
        history_dialog = HistoryDialog(self, self.user_id, theme=self.theme)
        history_dialog.exec_()
