import sys
import mysql.connector
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QLineEdit, QTextEdit, QHBoxLayout, QLabel, QFrame, 
                             QScrollArea, QSizePolicy, QSpacerItem, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from db2 import get_notes, add_note, delete_note, update_note, get_user_theme

class NotesApp(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.note_widgets = []
        self.cached_theme = None
        self.cached_notes = None
        self.editor = None
        self.initUI()
        self.load_user_theme()
        
    def initUI(self):
        self.setWindowTitle('Notes')
        self.setGeometry(100, 100, 1000, 500)
        self.layout = QVBoxLayout()

        # Add Note Button (+)
        self.add_note_button = QPushButton('+')
        self.add_note_button.setFixedSize(50, 50)
        self.add_note_button.clicked.connect(lambda: self.show_note_editor())
        self.layout.addWidget(self.add_note_button, alignment=Qt.AlignTop | Qt.AlignRight)

        # Horizontal Line
        self.horizontal_line = QFrame()
        self.horizontal_line.setFrameShape(QFrame.HLine)
        self.horizontal_line.setFrameShadow(QFrame.Plain)
        self.layout.addWidget(self.horizontal_line)

        # Notes Layout
        self.notes_layout = QVBoxLayout()
        self.notes_layout.setSpacing(15)
        self.notes_container = QWidget()
        self.notes_container.setLayout(self.notes_layout)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        self.scroll_area.setWidget(self.notes_container)
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)
        self.load_notes()

    def load_notes(self):
        """Load notes and update UI efficiently"""
        self.clear_note_widgets()
        
        try:
            # Get notes from database
            self.cached_notes = get_notes(self.user_id)
            
            # Create note widgets
            for note in self.cached_notes:
                self.add_note_widget(note)
        except Exception as e:
            print(f"Error loading notes: {e}")

    def clear_note_widgets(self):
        """Clear all note widgets from layout"""
        for i in reversed(range(self.notes_layout.count())): 
            widget = self.notes_layout.itemAt(i).widget()
            if widget is not None: 
                widget.deleteLater()
        
        self.note_widgets = []
    
    def add_note_widget(self, note):
        """Add a single note widget to the layout"""
        note_widget = QWidget()
        note_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        note_widget.setObjectName("note")
        note_layout = QVBoxLayout()

        title_label = QLabel(note['title'])
        title_label.setFont(QFont('Arial', 16))
        title_label.setWordWrap(True)
        note_layout.addWidget(title_label)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Plain)
        note_layout.addWidget(horizontal_line)

        button_layout = QHBoxLayout()

        edit_button = QPushButton('Edit')
        edit_button.clicked.connect(lambda _, n=note: self.show_note_editor(n))
        button_layout.addWidget(edit_button)

        spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        button_layout.addItem(spacer)

        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda _, nid=note['id'], w=note_widget: self.delete_note_widget(nid, w))
        button_layout.addWidget(delete_button)
        
        button_layout.setContentsMargins(10, 5, 10, 5)
        note_layout.addLayout(button_layout)
        note_widget.setLayout(note_layout)

        self.notes_layout.addWidget(note_widget, alignment=Qt.AlignTop)

        # Store references for theme updates
        self.note_widgets.append({
            'widget': note_widget,
            'title': title_label,
            'line': horizontal_line,
            'edit': edit_button,
            'delete': delete_button
        })

        if self.cached_theme:
            self.apply_theme_to_note(self.note_widgets[-1], self.cached_theme)

    def show_note_editor(self, note=None):
        self.editor = NoteEditor(self.user_id, self, note)
        if self.cached_theme:
            self.editor.apply_theme(self.cached_theme)
        self.editor.show()
        
    def delete_note_widget(self, note_id, widget=None):
        """Delete a note by ID"""
        try:
            delete_note(self.user_id, note_id)
            if widget:
                self.notes_layout.removeWidget(widget)
                widget.deleteLater()
            self.load_notes()
        except Exception as e:
            print(f"Error deleting note: {e}")
            QMessageBox.critical(self, "Error", f"Failed to delete note: {str(e)}")

    def load_user_theme(self):
        try:
            theme = get_user_theme(self.user_id)
            if theme:
                self.cached_theme = theme
                self.apply_theme(theme)
        except Exception as e:
            print(f"Error loading theme: {e}")
    
    def apply_theme(self, theme):
        """Apply theme to all UI elements"""
        if not theme:
            return
            
        _, color_1, color_2, color_3, color_4 = theme.values()

        # Main app styling
        self.setStyleSheet(f"QWidget {{ background-color: {color_3}; }}")

        self.add_note_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_2};
                color: white;
                border-radius: 25px;
                font-size: 30px;
            }}
            QPushButton:hover {{
                background-color: {color_1};
            }}
        """)

        # Divider styling
        self.horizontal_line.setStyleSheet(f"QFrame {{ background-color: {color_4}; color: {color_4}; }}")

        # Apply to all note widgets
        for note_widget in self.note_widgets:
            self.apply_theme_to_note(note_widget, theme)

        # Apply to editor if open
        if hasattr(self, 'editor') and self.editor:
            self.editor.apply_theme(theme)
    
    def apply_theme_to_note(self, note_widget, theme):
        """Apply theme to a single note widget"""
        if not theme:
            return
            
        _, color_1, color_2, color_3, color_4 = theme.values()
        
        # Widget styling
        note_widget['widget'].setStyleSheet(f"""
            QWidget#note {{
                border: 1px solid white;
                border-radius: 20px;
                padding: 5px;
                background-color: {color_2};
            }}
        """)
        
        # Title styling
        note_widget['title'].setStyleSheet("QLabel { color: #FFFFFF; padding: 10px; background: transparent; }")
        
        # Line styling
        note_widget['line'].setStyleSheet(f"QFrame {{ color: {color_4}; padding: 10px; border: none}}")

        button_style = f"""
            QPushButton {{
                background-color: {color_4};
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 5px;
                border: 1px solid white;
            }}
            QPushButton:hover {{
                background-color: {color_1};
            }}
        """
        
        note_widget['edit'].setStyleSheet(button_style)
        note_widget['delete'].setStyleSheet(button_style)

    def refresh_theme(self):
        self.load_user_theme()
        

class NoteEditor(QWidget):
    def __init__(self, user_id, notes_app, note=None):
        super().__init__()
        self.user_id = user_id
        self.notes_app = notes_app
        self.note = note
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Note Editor')
        self.setGeometry(400, 150, 600, 400)

        self.layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter title...")
        self.title_edit.setFont(QFont('Arial', 14))

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Write your note here...")
        self.content_edit.setFont(QFont('Arial', 14))

        if self.note:
            self.title_edit.setText(self.note['title'])
            self.content_edit.setText(self.note['content'])

        self.layout.addWidget(self.title_edit)
        self.layout.addWidget(self.content_edit)

        self.button_layout = QHBoxLayout()

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_note)
        self.button_layout.addWidget(self.save_button)

        if self.note:
            self.delete_button = QPushButton('Delete')
            self.delete_button.clicked.connect(self.delete_note)
            self.button_layout.addWidget(self.delete_button)

        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def apply_theme(self, theme):
        """Apply theme to editor dialog"""
        if not theme:
            return
            
        _, color_1, color_2, color_3, color_4 = theme.values()

        # Main styling
        self.setStyleSheet(f"QWidget {{ background-color: {color_3}; }}")

        self.title_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {color_2};
                border: 1px solid white;
                border-radius: 10px;
                padding: 8px;
                font-size: 16px;
                color: white;
            }}
        """)

        self.content_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {color_2};
                border: 1px solid white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: white;
            }}
        """)

        button_style = f"""
            QPushButton {{
                background-color: {color_4};
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 8px;
                border: 1px solid white;
            }}
            QPushButton:hover {{
                background-color: {color_1};
            }}
        """
        
        self.save_button.setStyleSheet(button_style)
        self.close_button.setStyleSheet(button_style)
        
        if hasattr(self, 'delete_button'):
            self.delete_button.setStyleSheet(button_style)

    def save_note(self):
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Missing Title", "Please enter a title for your note.")
            return

        try:
            if self.note:
                update_note(self.user_id, self.note['id'], title, content)
            else:
                add_note(self.user_id, title, content)
            
            self.notes_app.load_notes()
            self.close()
        except Exception as e:
            print(f"Error saving note: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save note: {str(e)}")

    def delete_note(self):
        if not self.note:
            return
            
        reply = QMessageBox.question(self, 'Confirm Deletion', 
                                     'Are you sure you want to delete this note?',
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
                                     
        if reply == QMessageBox.Yes:
            try:
                delete_note(self.user_id, self.note['id'])
                self.notes_app.load_notes()
                self.close()
            except Exception as e:
                print(f"Error deleting note: {e}")
                QMessageBox.critical(self, "Error", f"Failed to delete note: {str(e)}")