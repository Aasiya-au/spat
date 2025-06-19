import sys
import mysql.connector
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QMessageBox, QStackedWidget, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from db2 import signup, login, get_user_theme, get_developer
from profilee import Profile
from leaderboard import Leaderboard
from achievements import Achievements
from about import AboutPage
from notes import NotesApp
from session_timer import TimerUI
from themes import ThemeWidget
from home import Home
from flashcards import FlashcardsApp
from todo_list import TodoList
from chatbot import ChatBot
from dev_view import DeveloperDashboard

def get_colors(): #default colours for splash and auth screens
    color_1 = "#FFEBD8"
    color_2 = "#89B9AD"
    color_3 = "#C7DCA7"
    color_4 = "#FFC5C5"
    return color_1, color_2, color_3, color_4

class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super(SplashScreen, self).__init__(parent)
        self.color_1, self.color_2, self.color_3, self.color_4 = get_colors()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Study Planner and Tracker")
        self.setGeometry(200, 80, 1000, 600)
        
        # Main layout
        layout = QVBoxLayout()

        title = QLabel("Study Planner and Tracker")
        title.setStyleSheet(f"""
            font-size: 36px;
            font-weight: bold;
            color: {self.color_2};
            margin: 50px 0;
        """)
        title.setAlignment(Qt.AlignCenter)

        play_button = QPushButton("Start")
        play_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color_3};
                color: {self.color_2};
                border: none;
                border-radius: 25px;
                padding: 15px 30px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color_4};
            }}
        """)
        play_button.setCursor(Qt.PointingHandCursor)
        play_button.setFixedWidth(150)
        play_button.clicked.connect(self.openAuthScreen)
        
        # Add widgets to layout
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addStretch(1)
        
        # Create a layout for the button to center it
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(play_button)
        button_layout.addStretch(1)
        
        layout.addLayout(button_layout)
        layout.addStretch(2)
        
        self.setLayout(layout)

        self.setStyleSheet(f"background-color: {self.color_1};")

    def openAuthScreen(self):
        self.auth_app = AuthApp()
        self.auth_app.show()
        self.close()

class AuthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.color_1, self.color_2, self.color_3, self.color_4 = get_colors()
        self.text_box_width = 350
        self.label_font_size = 14
        self.button_width = 150

        self.initUI()
        self.applyTheme()

    def initUI(self):
        self.setWindowTitle("Authentication System")
        self.setGeometry(200, 80, 1000, 600)

        # Create stacked widget to manage multiple pages
        self.stacked_widget = QStackedWidget()

        self.signup_page = self.createSignupPage()
        self.login_page = self.createLoginPage()
        self.dev_login_page = self.createDevLoginPage()

        self.stacked_widget.addWidget(self.signup_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.dev_login_page)
        
        # Set layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        
        # Start with signup page
        self.stacked_widget.setCurrentIndex(0)

    def applyTheme(self):
        # Set application-wide palette
        palette = QPalette()
        
        # Set window background color (primary color)
        palette.setColor(QPalette.Window, QColor(self.color_1))

        palette.setColor(QPalette.WindowText, QColor(self.color_2))
        palette.setColor(QPalette.Text, QColor(self.color_2))

        palette.setColor(QPalette.Button, QColor(self.color_3))
        palette.setColor(QPalette.ButtonText, QColor(self.color_2))

        palette.setColor(QPalette.Base, QColor("#FFFFFF"))  # White background for input fields
        
        # Apply palette to application
        self.setPalette(palette)
        
        # Style buttons
        button_style = f"""
            QPushButton {{
                background-color: {self.color_3};
                color: {self.color_2};
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: {self.label_font_size}px;
            }}
            QPushButton:hover {{
                background-color: {self.color_4};
            }}
        """
        
        # Style input fields
        input_style = f"""
            QLineEdit {{
                border: 1px solid {self.color_4};
                border-radius: 4px;
                padding: 6px;
                background-color: white;
            }}
            QLineEdit:focus {{
                border: 2px solid {self.color_4};
            }}
        """
        
        # Style labels
        label_style = f"""
            QLabel {{
                color: {self.color_2};
                font-size: {self.label_font_size}px;
            }}
        """
        
        # Apply styles to specific widgets
        self.signup_button.setStyleSheet(button_style)
        self.login_button.setStyleSheet(button_style)
        self.dev_login_button.setStyleSheet(button_style)
        
        for label in [self.label_username, self.label_email, self.label_password,
                 self.login_label_username, self.login_label_password, self.dev_login_label_username]:
            label.setStyleSheet(label_style)

        for widget in [self.input_username, self.input_email, self.input_password,
                      self.login_input_username, self.login_input_password, self.dev_login_input_username]:
            widget.setStyleSheet(input_style)
            widget.setFixedWidth(self.text_box_width)
        
        self.input_username.setFixedWidth(200)
        self.input_email.setFixedWidth(200)
        self.input_password.setFixedWidth(200)
        self.login_input_username.setFixedWidth(200)
        self.login_input_password.setFixedWidth(200)
        self.dev_login_input_username.setFixedWidth(200)

    def createSignupPage(self):
        page = QWidget()
        
        # Create widgets
        title_label = QLabel("Create an Account")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; margin-bottom: 15px; color: {self.color_2};")
        
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Enter username")

        self.label_email = QLabel("Email:")
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Enter email address")

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Enter password (min 8 characters)")
        self.input_password.setEchoMode(QLineEdit.Password)  # Hide password input

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        self.signup_button.clicked.connect(self.handle_signup)
        
        # Create login navigation section
        login_nav_layout = QHBoxLayout()
        login_nav_label = QLabel("Already have an account?")
        login_nav_label.setStyleSheet(f"font-size: {self.label_font_size}px;")
        go_to_login_button = QPushButton("Login")
        go_to_login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.color_4};
                font-weight: bold;
                text-decoration: underline;
                border: none;
            }}
            QPushButton:hover {{
                color: {self.color_2};
            }}
        """)
        go_to_login_button.setCursor(Qt.PointingHandCursor)
        go_to_login_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        go_to_login_button.setFixedWidth(100)
        
        login_nav_layout.addWidget(login_nav_label)
        login_nav_layout.addWidget(go_to_login_button)
        login_nav_layout.setAlignment(Qt.AlignCenter)

        # Create dev login navigation section
        dev_login_nav_layout = QHBoxLayout()
        dev_login_nav_label = QLabel("Are you a developer?")
        dev_login_nav_label.setStyleSheet(f"font-size: {self.label_font_size}px;")
        go_to_dev_login_button = QPushButton("Developer Login")
        go_to_dev_login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.color_4};
                font-weight: bold;
                text-decoration: underline;
                border: none;
            }}
            QPushButton:hover {{
                color: {self.color_2};
            }}
        """)
        go_to_dev_login_button.setCursor(Qt.PointingHandCursor)
        # Fixed: Change index to 2 for developer login page
        go_to_dev_login_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        go_to_dev_login_button.setFixedWidth(150)  # Increased to fit text better
        
        dev_login_nav_layout.addWidget(dev_login_nav_label)
        dev_login_nav_layout.addWidget(go_to_dev_login_button)
        dev_login_nav_layout.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.label_username)
        form_layout.addWidget(self.input_username)
        form_layout.addWidget(self.label_email)
        form_layout.addWidget(self.input_email)
        form_layout.addWidget(self.label_password)
        form_layout.addWidget(self.input_password)
        form_layout.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(form_layout)
        layout.addSpacing(10)
    
        # Add button with center alignment
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.signup_button)
        button_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout)
    
        layout.addSpacing(20)
        layout.addLayout(login_nav_layout)
        layout.addLayout(dev_login_nav_layout)
        
        page.setLayout(layout)
        return page

    def createLoginPage(self):
        page = QWidget()
        
        # Create widgets
        title_label = QLabel("Login to Your Account")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; margin-bottom: 15px; color: {self.color_2};")
        
        self.login_label_username = QLabel("Username:")
        self.login_input_username = QLineEdit()
        self.login_input_username.setPlaceholderText("Enter your username")

        self.login_label_password = QLabel("Password:")
        self.login_input_password = QLineEdit()
        self.login_input_password.setPlaceholderText("Enter your password")
        self.login_input_password.setEchoMode(QLineEdit.Password)  # Hide password input

        self.login_button = QPushButton("Login")
        self.login_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        self.login_button.clicked.connect(self.handle_login)
        
        # Create signup navigation section
        signup_nav_layout = QHBoxLayout()
        signup_nav_label = QLabel("Don't have an account?")
        signup_nav_label.setStyleSheet(f"font-size: {self.label_font_size}px;")
        go_to_signup_button = QPushButton("Sign Up")
        go_to_signup_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.color_4};
                font-weight: bold;
                text-decoration: underline;
                border: none;
            }}
            QPushButton:hover {{
                color: {self.color_2};
            }}
        """)
        go_to_signup_button.setCursor(Qt.PointingHandCursor)
        go_to_signup_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        go_to_signup_button.setFixedWidth(100)
        
        # Added: Developer login button in regular login page
        go_to_dev_login_button = QPushButton("Developer Login")
        go_to_dev_login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.color_4};
                font-weight: bold;
                text-decoration: underline;
                border: none;
            }}
            QPushButton:hover {{
                color: {self.color_2};
            }}
        """)
        go_to_dev_login_button.setCursor(Qt.PointingHandCursor)
        go_to_dev_login_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        go_to_dev_login_button.setFixedWidth(150)
        
        signup_nav_layout.addWidget(signup_nav_label)
        signup_nav_layout.addWidget(go_to_signup_button)
        signup_nav_layout.addWidget(go_to_dev_login_button)  # Added developer login button
        signup_nav_layout.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)

        # Create form layout with centered widgets
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.login_label_username)
        form_layout.addWidget(self.login_input_username)
        form_layout.addWidget(self.login_label_password)
        form_layout.addWidget(self.login_input_password)
        form_layout.setAlignment(Qt.AlignCenter)  # Center the form elements
    
        layout.addLayout(form_layout)
        layout.addSpacing(10)
    
        # Add button with center alignment
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.setAlignment(Qt.AlignCenter)  # Center the button
        layout.addLayout(button_layout)
    
        layout.addSpacing(20)
        layout.addLayout(signup_nav_layout)
        
        page.setLayout(layout)
        return page

    def createDevLoginPage(self):
        page = QWidget()
        
        # Create widgets
        title_label = QLabel("Developer Login")  # Changed title to be more specific
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; margin-bottom: 15px; color: {self.color_2};")
        
        self.dev_login_label_username = QLabel("Name:")
        self.dev_login_input_username = QLineEdit()
        self.dev_login_input_username.setPlaceholderText("Enter your full name")

        self.dev_login_button = QPushButton("Login")
        self.dev_login_button.setCursor(Qt.PointingHandCursor)  # Change cursor on hover
        self.dev_login_button.clicked.connect(self.handle_dev_login)
        
        # Create navigation section for regular login and signup
        nav_layout = QHBoxLayout()
        
        back_to_login_button = QPushButton("User Login")
        back_to_login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.color_4};
                font-weight: bold;
                text-decoration: underline;
                border: none;
            }}
            QPushButton:hover {{
                color: {self.color_2};
            }}
        """)
        back_to_login_button.setCursor(Qt.PointingHandCursor)
        back_to_login_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        back_to_login_button.setFixedWidth(100)
        
        go_to_signup_button = QPushButton("Sign Up")
        go_to_signup_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.color_4};
                font-weight: bold;
                text-decoration: underline;
                border: none;
            }}
            QPushButton:hover {{
                color: {self.color_2};
            }}
        """)
        go_to_signup_button.setCursor(Qt.PointingHandCursor)
        go_to_signup_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        go_to_signup_button.setFixedWidth(100)
        
        nav_layout.addWidget(back_to_login_button)
        nav_layout.addWidget(go_to_signup_button)
        nav_layout.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)

        # Create form layout with centered widgets
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.dev_login_label_username)
        form_layout.addWidget(self.dev_login_input_username)
        form_layout.setAlignment(Qt.AlignCenter)  # Center the form elements
    
        layout.addLayout(form_layout)
        layout.addSpacing(10)
    
        # Add button with center alignment
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.dev_login_button)
        button_layout.setAlignment(Qt.AlignCenter)  # Center the button
        layout.addLayout(button_layout)
    
        layout.addSpacing(20)
        layout.addLayout(nav_layout)
        
        page.setLayout(layout)
        return page

    def handle_signup(self):
        username = self.input_username.text()
        email = self.input_email.text()
        password = self.input_password.text()

        # Basic client-side validation
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        # Call the backend signup function
        result = signup(username, email, password)

        # Handle different response types
        if isinstance(result, str):  # If result is an error message
            QMessageBox.warning(self, "Error", result)
        elif isinstance(result, Exception):  # If an exception occurred
            QMessageBox.critical(self, "Error", f"An error occurred: {str(result)}")
        else:  # If signup was successful
            QMessageBox.information(self, "Success", "Account created successfully!")
            # Launch the main application
            self.main_app = MainApp(result)
            self.main_app.show()
            self.hide()  # Hide signup window instead of closing it

    def handle_login(self):
        username = self.login_input_username.text()
        password = self.login_input_password.text()
        
        # Basic client-side validation
        if not username or not password:
            QMessageBox.warning(self, "Error", "Both username and password are required")
            return
            
        # Call the backend login function
        result = login(username, password)
        
        # Handle different response types
        if isinstance(result, str):  # If result is an error message
            QMessageBox.warning(self, "Error", result)
        elif isinstance(result, Exception):  # If an exception occurred
            QMessageBox.critical(self, "Error", f"An error occurred: {str(result)}")
        else:  # If login was successful
            QMessageBox.information(self, "Success", f"Welcome back, {username}!")
            # Launch the main application
            self.main_app = MainApp(result)
            self.main_app.show()
            self.hide()  # Hide login window instead of closing it

    def handle_dev_login(self):
        username = self.dev_login_input_username.text()
        
        # Added client-side validation
        if not username:
            QMessageBox.warning(self, "Error", "Developer name is required")
            return
            
        result = get_developer(username)
        
        # Handle different response types
        if isinstance(result, str):  # If result is an error message
            QMessageBox.warning(self, "Error", result)
        elif isinstance(result, Exception):  # If an exception occurred
            QMessageBox.critical(self, "Error", f"An error occurred: {str(result)}")
        else:  # If login was successful
            QMessageBox.information(self, "Success", f"Welcome back, {username}!")
            # Launch the main application
            self.main_app = DeveloperDashboard()
            self.main_app.show()
            self.hide()  # Hide login window instead of closing it

class MainApp(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.username = self.user["username"]
        self.user_id = self.user["id"]
        # Store references to all buttons
        self.panel_buttons = {}
        self.active_panel = "Home"  # Track currently active panel
        self.load_user_theme()
        self.initUI()
        # Now apply the theme after UI elements have been created
        self.apply_theme()
        
    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        if theme:
            _, self.color_1, self.color_2, self.color_3, self.color_4 = theme.values()
    
    def apply_theme(self):
        # Make sure the UI has been initialized before applying theme
        if not hasattr(self, 'sidebar_frame'):
            return
            
        # Basic application styling
        self.setStyleSheet(f"background-color: {self.color_1};")
        self.sidebar_frame.setStyleSheet(f"background-color: {self.color_3};")
        
        if hasattr(self, 'welcome_label'):
            self.welcome_label.setStyleSheet(f"""
                font-size: 16px;
                font-weight: bold;
                color: {self.color_2};
                padding: 10px 0;
            """)
            
        if hasattr(self, 'logout_button'):
            self.logout_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.color_2};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 12px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.color_1};
                }}
            """)
        
        # Update all sidebar button styles
        for panel_name, button in self.panel_buttons.items():
            if panel_name == self.active_panel:
                button.setStyleSheet(self.get_active_button_style())
            else:
                button.setStyleSheet(self.get_inactive_button_style())

    def get_active_button_style(self):
        """Style for the active button"""
        return f"""
            QPushButton {{
                background-color: {self.color_4};
                color: {self.color_2};
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
                text-align: left;
                font-weight: bold;
            }}
        """
    
    def get_inactive_button_style(self):
        """Style for inactive buttons"""
        return f"""
            QPushButton {{
                background-color: {self.color_1};
                color: {self.color_2};
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
                text-align: left;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.color_4};
            }}
        """

    def refresh_theme(self):
        self.load_user_theme()
        self.apply_theme()

    def initUI(self):
        self.setWindowTitle("Study Planner App")
        self.setGeometry(200, 50, 1000, 600)
        
        # Create main layout
        main_layout = QHBoxLayout()
        
        theme_widget = ThemeWidget(self.user_id)
        for button in theme_widget.theme_button_list + theme_widget.character_button_list:
            button.clicked.connect(self.refresh_themes)
        
        home_widget = Home(self.user_id)
        self.home_widget = home_widget

        achievements_widget = Achievements(self.user_id)
        self.achievements_widget = achievements_widget

        profile_widget = Profile(self.username)
        self.profile_widget = profile_widget

        leaderboard_widget = Leaderboard(self.user_id)
        self.leaderboard_widget = leaderboard_widget

        session_widget = TimerUI(self.user)
        self.session_widget = session_widget

        notes_widget = NotesApp(self.user_id)
        self.notes_widget = notes_widget

        flashcards_widget = FlashcardsApp(self.user_id)
        self.flashcards_widget = flashcards_widget

        about_widget = AboutPage(self.user_id)
        self.about_widget = about_widget

        todo_widget = TodoList(self.user_id)
        self.todo_widget = todo_widget

        chatbot_widget = ChatBot(self.user_id)
        self.chatbot_widget = chatbot_widget

        # Create sidebar buttons/panels
        self.panels = {
            "Home": home_widget,
            "Profile": profile_widget,
            "Notes": notes_widget,
            "Study Session": session_widget,
            "Flashcards": flashcards_widget,
            "To-Do List": todo_widget,
            "Chat-Bot": chatbot_widget,
            "Achievements": achievements_widget,
            "Appearance": theme_widget,
            "Leaderboard": leaderboard_widget,
            "About": about_widget
        }
        
        # Create stacked widget for multiple pages
        self.stacked_widget = QStackedWidget()
        for page in self.panels.values():
            self.stacked_widget.addWidget(page)
        
        # Create and add sidebar buttons
        self.sidebar_frame = QWidget()
        self.sidebar_frame.setFixedWidth(200)  # Set width of sidebar
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setAlignment(Qt.AlignTop)
        
        # Add welcome message at the top of sidebar
        self.welcome_label = QLabel(f"Welcome, {self.username}!")
        sidebar_layout.addWidget(self.welcome_label)
        sidebar_layout.addSpacing(20)
        
        # Add all panel buttons
        for i, panel_name in enumerate(self.panels.keys()):
            button = QPushButton(panel_name)
            button.setCursor(Qt.PointingHandCursor)
            # Connect button to its respective page
            button.clicked.connect(lambda checked, name=panel_name: self.switch_to_panel(name))
            sidebar_layout.addWidget(button)
            self.panel_buttons[panel_name] = button

        self.switch_to_panel("Home")

        # Add logout button at the bottom
        sidebar_layout.addStretch()
        self.logout_button = QPushButton("Logout")
        self.logout_button.setCursor(Qt.PointingHandCursor)
        self.logout_button.clicked.connect(self.handleLogout)
        sidebar_layout.addWidget(self.logout_button)
        
        # Add sidebar and content area to main layout
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.stacked_widget)
        
        self.setLayout(main_layout)
    
    def switch_to_panel(self, panel_name):
        """Switch to a panel by name"""
        if panel_name not in self.panels:
            return
            
        # Track active panel
        self.active_panel = panel_name
            
        # Find the index of the panel
        panel_index = list(self.panels.keys()).index(panel_name)
        
        # Update stacked widget
        self.stacked_widget.setCurrentIndex(panel_index)
        
        # Update just the button styles instead of all theme elements
        # Reset all buttons to normal style
        for name, button in self.panel_buttons.items():
            if name == panel_name:
                button.setStyleSheet(self.get_active_button_style())
            else:
                button.setStyleSheet(self.get_inactive_button_style())
    
    def refresh_themes(self):
        self.refresh_theme()
        """Refresh themes for components that support dynamic theming"""
        if hasattr(self.home_widget, 'refresh_theme'):
            self.home_widget.refresh_theme()
        
        if hasattr(self.achievements_widget, 'refresh_theme'):
            self.achievements_widget.refresh_theme()
        
        if hasattr(self.profile_widget, 'refresh_theme'):
            self.profile_widget.refresh_theme()
    
        if hasattr(self.leaderboard_widget, 'refresh_theme'):
            self.leaderboard_widget.refresh_theme()
    
        if hasattr(self.session_widget, 'refresh_theme'):
            self.session_widget.refresh_theme()
    
        if hasattr(self.flashcards_widget, 'refresh_theme'):
            self.flashcards_widget.refresh_theme()
        
        if hasattr(self.notes_widget, 'refresh_theme'):
            self.notes_widget.refresh_theme()

        if hasattr(self.about_widget, 'refresh_theme'):
            self.about_widget.refresh_theme()
        
        if hasattr(self.todo_widget, 'refresh_theme'):
            self.todo_widget.refresh_theme()
        
        if hasattr(self.chatbot_widget, 'refresh_theme'):
            self.chatbot_widget.refresh_theme()
        
    def createPageWithText(self, page_name):
        page = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel(f"{page_name} Page")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {self.color_2};
        """)
        title.setAlignment(Qt.AlignCenter)
        
        content = QLabel(f"This is the {page_name} page. Content coming soon!")
        content.setStyleSheet(f"""
            font-size: 18px;
            color: {self.color_2};
            margin-top: 20px;
        """)
        content.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(content)
        page.setLayout(layout)
        return page
    
    def handleLogout(self):
        # Show confirmation dialog
        reply = QMessageBox.question(
            self, 'Logout Confirmation',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Close this window and show login window again
            self.parent_window = SplashScreen()
            self.parent_window.show()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())