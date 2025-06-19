import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QListWidget, QListWidgetItem,
    QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView
)
from PyQt5.QtCore import Qt
from db2 import (
    get_error_logs, get_action_logs, get_user_action_logs, get_api_logs,
    get_user_logins, get_logins
)

class DeveloperDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Developer Dashboard")
        self.setGeometry(200, 80, 1000, 600)

        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar for navigation
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.addItem("Home")
        self.sidebar.addItem("Error Logs")
        self.sidebar.addItem("User Action Logs")
        self.sidebar.addItem("API Logs")
        self.sidebar.addItem("Logins")
        self.sidebar.currentRowChanged.connect(self.display_page)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2A2F3E;
                color: #D3D3D3;
                font-size: 16px;
                border: none;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #3A3F4E;
            }
            QListWidget::item:selected {
                background-color: #3A3F4E;
                color: #FFFFFF;
            }
            QListWidget::item:hover {
                background-color: #353A49;
            }
        """)
        main_layout.addWidget(self.sidebar)

        # Stacked widget for pages
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("""
            QStackedWidget {
                background-color: #1F232A;
                color: #D3D3D3;
            }
        """)
        main_layout.addWidget(self.pages)

        # Create pages
        self.pages.addWidget(self.create_home_page())
        self.pages.addWidget(self.create_error_logs_page())
        self.pages.addWidget(self.create_user_logs_page())
        self.pages.addWidget(self.create_api_logs_page())
        self.pages.addWidget(self.create_logins_page())

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        label = QLabel("Welcome to the Developer Dashboard")
        label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #FFFFFF;
            }
        """)
        layout.addWidget(label)
        layout.addStretch()
        return page

    def create_error_logs_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        label = QLabel("Error Logs")
        label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
            }
        """)
        layout.addWidget(label)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Timestamp", "Location", "Message"])
        table.setRowCount(0)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.horizontalHeader().setStretchLastSection(True)
        table.setWordWrap(True)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #2A2F3E;
                color: #D3D3D3;
                border: none;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3A3F4E;
            }
            QHeaderView::section {
                background-color: #3A3F4E;
                color: #FFFFFF;
                padding: 10px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #4A4F5E;
                color: #FFFFFF;
            }
        """)
        table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #3A3F4E;
                color: #FFFFFF;
                padding: 10px;
                border: none;
            }
        """)
        table.setSizePolicy(table.sizePolicy().horizontalPolicy(), table.sizePolicy().Expanding)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        error_logs = get_error_logs()
        table.setRowCount(len(error_logs))
        for row, log in enumerate(error_logs):
            item_timestamp = QTableWidgetItem(str(log['timestamp']))
            item_timestamp.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_location = QTableWidgetItem(log['location'])
            item_location.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_message = QTableWidgetItem(log['message'])
            item_message.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            table.setItem(row, 0, item_timestamp)
            table.setItem(row, 1, item_location)
            table.setItem(row, 2, item_message)

            table.resizeRowToContents(row)

        layout.addWidget(table)
        return page

    def create_user_logs_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        label = QLabel("User Action Logs")
        label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
            }
        """)
        layout.addWidget(label)

        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by ID or Username:")
        filter_label.setStyleSheet("""
            QLabel {
                color: #D3D3D3;
                font-size: 14px;
            }
        """)
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Enter ID or Username")
        self.user_id_input.setStyleSheet("""
            QLineEdit {
                background-color: #2A2F3E;
                color: #D3D3D3;
                border: 1px solid #3A3F4E;
                border-radius: 5px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 1px solid #5A5F6E;
            }
        """)
        filter_button = QPushButton("Filter")
        clear_button = QPushButton("Clear")
        for button in (filter_button, clear_button):
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3A3F4E;
                    color: #FFFFFF;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #4A4F5E;
                }
                QPushButton:pressed {
                    background-color: #5A5F6E;
                }
            """)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.user_id_input)
        filter_layout.addWidget(filter_button)
        filter_layout.addWidget(clear_button)
        layout.addLayout(filter_layout)

        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(6)
        self.logs_table.setHorizontalHeaderLabels(["Timestamp", "User ID", "Username", "Action Name", "Entity Name", "Target ID"])
        self.logs_table.setRowCount(0)
        self.logs_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.logs_table.horizontalHeader().setStretchLastSection(True)
        self.logs_table.setWordWrap(True)
        self.logs_table.setStyleSheet("""
            QTableWidget {
                background-color: #2A2F3E;
                color: #D3D3D3;
                border: none;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3A3F4E;
            }
            QHeaderView::section {
                background-color: #3A3F4E;
                color: #FFFFFF;
                padding: 10px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #4A4F5E;
                color: #FFFFFF;
            }
        """)
        self.logs_table.setSizePolicy(self.logs_table.sizePolicy().horizontalPolicy(), self.logs_table.sizePolicy().Expanding)
        self.logs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_user_logs()

        filter_button.clicked.connect(self.filter_user_logs)
        clear_button.clicked.connect(self.populate_user_logs)

        layout.addWidget(self.logs_table)
        return page

    def populate_user_logs(self):
        self.logs_table.setRowCount(0)
        action_logs = get_action_logs()
        self.logs_table.setRowCount(len(action_logs))
        for row, log in enumerate(action_logs):
            item_timestamp = QTableWidgetItem(str(log['timestamp']))
            item_timestamp.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_user_id = QTableWidgetItem(str(log['user_id']))
            item_user_id.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_username = QTableWidgetItem(log['username'])
            item_username.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_action_name = QTableWidgetItem(log['action_name'])
            item_action_name.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_entity_name = QTableWidgetItem(log['entity_name'])
            item_entity_name.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_target_id = QTableWidgetItem(str(log['target_id']))
            item_target_id.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.logs_table.setItem(row, 0, item_timestamp)
            self.logs_table.setItem(row, 1, item_user_id)
            self.logs_table.setItem(row, 2, item_username)
            self.logs_table.setItem(row, 3, item_action_name)
            self.logs_table.setItem(row, 4, item_entity_name)
            self.logs_table.setItem(row, 5, item_target_id)

            self.logs_table.resizeRowToContents(row)

    def filter_user_logs(self):
        identifier = self.user_id_input.text().strip()
        if not identifier:
            self.populate_user_logs()
            return

        self.logs_table.setRowCount(0)
        action_logs = get_user_action_logs(identifier)
        self.logs_table.setRowCount(len(action_logs))
        for row, log in enumerate(action_logs):
            item_timestamp = QTableWidgetItem(str(log['timestamp']))
            item_timestamp.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_user_id = QTableWidgetItem(str(log['user_id']))
            item_user_id.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_username = QTableWidgetItem(log['username'])
            item_username.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_action_name = QTableWidgetItem(log['action_name'])
            item_action_name.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_entity_name = QTableWidgetItem(log['entity_name'])
            item_entity_name.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_target_id = QTableWidgetItem(str(log['target_id']))
            item_target_id.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.logs_table.setItem(row, 0, item_timestamp)
            self.logs_table.setItem(row, 1, item_user_id)
            self.logs_table.setItem(row, 2, item_username)
            self.logs_table.setItem(row, 3, item_action_name)
            self.logs_table.setItem(row, 4, item_entity_name)
            self.logs_table.setItem(row, 5, item_target_id)

            self.logs_table.resizeRowToContents(row)

    def create_api_logs_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        label = QLabel("API Logs")
        label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
            }
        """)
        layout.addWidget(label)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["id", "timestamp", "api_endpoint", "request_data", "response_status"])
        table.setRowCount(0)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.horizontalHeader().setStretchLastSection(True)
        table.setWordWrap(True)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #2A2F3E;
                color: #D3D3D3;
                border: none;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3A3F4E;
            }
            QHeaderView::section {
                background-color: #3A3F4E;
                color: #FFFFFF;
                padding: 10px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #4A4F5E;
                color: #FFFFFF;
            }
        """)
        table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #3A3F4E;
                color: #FFFFFF;
                padding: 10px;
                border: none;
            }
        """)
        table.setSizePolicy(table.sizePolicy().horizontalPolicy(), table.sizePolicy().Expanding)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        api_logs = get_api_logs()
        table.setRowCount(len(api_logs))
        for row, log in enumerate(api_logs):
            item_id = QTableWidgetItem(str(log['id']))
            item_id.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_timestamp = QTableWidgetItem(str(log['timestamp']))
            item_timestamp.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_endpoint = QTableWidgetItem(log['api_endpoint'])
            item_endpoint.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            
            # Truncate request_data to 50 characters and add ellipsis
            request_data = log['request_data']
            display_text = request_data[:50] + "..." if len(request_data) > 50 else request_data
            item_request = QTableWidgetItem(display_text)
            item_request.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            # Set tooltip with full request data
            item_request.setToolTip(request_data)
            
            item_status = QTableWidgetItem(log['response_status'])
            item_status.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            table.setItem(row, 0, item_id)
            table.setItem(row, 1, item_timestamp)
            table.setItem(row, 2, item_endpoint)
            table.setItem(row, 3, item_request)
            table.setItem(row, 4, item_status)

            table.resizeRowToContents(row)

        layout.addWidget(table)
        return page

    def create_logins_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        label = QLabel("Login Logs")
        label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
            }
        """)
        layout.addWidget(label)

        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by User ID or Username:")
        filter_label.setStyleSheet("""
            QLabel {
                color: #D3D3D3;
                font-size: 14px;
            }
        """)
        self.user_id_input_login = QLineEdit()
        self.user_id_input_login.setPlaceholderText("Enter User ID or Username")
        self.user_id_input_login.setStyleSheet("""
            QLineEdit {
                background-color: #2A2F3E;
                color: #D3D3D3;
                border: 1px solid #3A3F4E;
                border-radius: 5px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 1px solid #5A5F6E;
            }
        """)
        filter_button = QPushButton("Filter")
        clear_button = QPushButton("Clear")
        for button in (filter_button, clear_button):
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3A3F4E;
                    color: #FFFFFF;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #4A4F5E;
                }
                QPushButton:pressed {
                    background-color: #5A5F6E;
                }
            """)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.user_id_input_login)
        filter_layout.addWidget(filter_button)
        filter_layout.addWidget(clear_button)
        layout.addLayout(filter_layout)

        self.logins_table = QTableWidget()
        self.logins_table.setColumnCount(3)
        self.logins_table.setHorizontalHeaderLabels(["User ID", "Username", "Login Date"])
        self.logins_table.setRowCount(0)
        self.logins_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.logins_table.horizontalHeader().setStretchLastSection(True)
        self.logins_table.setWordWrap(True)
        self.logins_table.setStyleSheet("""
            QTableWidget {
                background-color: #2A2F3E;
                color: #D3D3D3;
                border: none;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3A3F4E;
            }
            QHeaderView::section {
                background-color: #3A3F4E;
                color: #FFFFFF;
                padding: 10px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #4A4F5E;
                color: #FFFFFF;
            }
        """)
        self.logins_table.setSizePolicy(self.logins_table.sizePolicy().horizontalPolicy(), self.logins_table.sizePolicy().Expanding)
        self.logins_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_logins()

        filter_button.clicked.connect(self.filter_logins)
        clear_button.clicked.connect(self.populate_logins)

        layout.addWidget(self.logins_table)
        return page

    def populate_logins(self):
        self.logins_table.setRowCount(0)
        logins = get_logins()
        self.logins_table.setRowCount(len(logins))
        for row, log in enumerate(logins):
            item_user_id = QTableWidgetItem(str(log['user_id']))
            item_user_id.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_username = QTableWidgetItem(log['username'])
            item_username.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_login_date = QTableWidgetItem(str(log['login_date']))
            item_login_date.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.logins_table.setItem(row, 0, item_user_id)
            self.logins_table.setItem(row, 1, item_username)
            self.logins_table.setItem(row, 2, item_login_date)

            self.logins_table.resizeRowToContents(row)

    def filter_logins(self):
        identifier = self.user_id_input_login.text().strip()
        if not identifier:
            self.populate_logins()
            return

        self.logins_table.setRowCount(0)
        logins = get_user_logins(identifier)
        self.logins_table.setRowCount(len(logins))
        for row, log in enumerate(logins):
            item_user_id = QTableWidgetItem(str(log['user_id']))
            item_user_id.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_username = QTableWidgetItem(log['username'])
            item_username.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_login_date = QTableWidgetItem(str(log['login_date']))
            item_login_date.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.logins_table.setItem(row, 0, item_user_id)
            self.logins_table.setItem(row, 1, item_username)
            self.logins_table.setItem(row, 2, item_login_date)

            self.logins_table.resizeRowToContents(row)

    def display_page(self, index):
        self.pages.setCurrentIndex(index)