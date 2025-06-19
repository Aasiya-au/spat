import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QComboBox, QFrame, QScrollArea, QMessageBox, QTextEdit, QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from db2 import add_flashcard, update_flashcard, get_subjects, get_user_theme
from db2 import get_flashcards_by_subject, get_all_flashcards, delete_flashcard


class FlashcardsApp(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.cached_theme = None
        self.load_user_theme()
        self.initUI()
        self.apply_theme(self.cached_theme)

    def initUI(self):
        self.setWindowTitle("Flashcards")
        self.setGeometry(100, 100, 1000, 500)

        self.layout = QVBoxLayout()

        # Subject Filter
        self.subject_dropdown = QComboBox()
        self.subject_dropdown.addItem("All Subjects", None)  # Default: Show all
        self.subject_dropdown.currentIndexChanged.connect(self.load_flashcards)
        self.layout.addWidget(self.subject_dropdown)
        self.load_subjects()

        # Flashcards Container (Scrollable)
        self.scroll_area = QScrollArea()
        self.flashcards_container = QWidget()
        self.flashcards_layout = QGridLayout(self.flashcards_container)
        self.flashcards_layout.setSpacing(10)
        self.scroll_area.setWidget(self.flashcards_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        self.layout.addWidget(self.scroll_area)

        # Add Flashcard Button
        self.add_flashcard_button = QPushButton("+ Add Flashcard")
        self.add_flashcard_button.clicked.connect(self.add_flashcard)
        self.layout.addWidget(self.add_flashcard_button, alignment=Qt.AlignRight)

        self.setLayout(self.layout)
        self.load_flashcards()

    def load_subjects(self):
        subjects = get_subjects(user_id=self.user_id)
        for subject in subjects:
            self.subject_dropdown.addItem(subject['name'], subject['id'])

    def load_flashcards(self):
        # Clear old flashcard widget references
        if hasattr(self, 'flashcard_widgets'):
            self.flashcard_widgets.clear()

        for i in reversed(range(self.flashcards_layout.count())):
            widget = self.flashcards_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        subject_id = self.subject_dropdown.currentData()
        flashcards = get_flashcards_by_subject(self.user_id, subject_id) if subject_id else get_all_flashcards(self.user_id)

        available_width = self.width()  # ✨ Use self.width() here
        card_width = 250
        spacing = self.flashcards_layout.spacing()
        total_card_space = card_width + spacing
        columns = max(1, available_width // total_card_space)

        row = 0
        col = 0
        for flashcard_text in flashcards:
            card = self.add_flashcard_widget(flashcard_text)
            self.flashcards_layout.addWidget(card, row, col, alignment=Qt.AlignTop)

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def resizeEvent(self, event):
        self.load_flashcards()
        super().resizeEvent(event)

    def add_flashcard_widget(self, flashcard):
        card_widget = QWidget()
        card_widget.setFixedHeight(300)
        card_widget.setFixedWidth(250)

        card_layout = QVBoxLayout(card_widget)

        question_container = QFrame()
        question_layout = QVBoxLayout(question_container)
        question_layout.setContentsMargins(10, 10, 10, 10)
        question_layout.setSpacing(5)

        question_label = QLabel(f"Q: {flashcard['question']}")
        question_label.setFont(QFont("Arial", 12))
        question_label.setWordWrap(True)
        question_label.setStyleSheet("QLabel { color: white; border: none; }")
        question_layout.addWidget(question_label)

        answer_label = QLabel(f"A: {flashcard['answer']}")
        answer_label.setFont(QFont("Arial", 11))
        answer_label.setStyleSheet("QLabel { color: white; border: none; }")
        answer_label.setWordWrap(True)
        answer_label.setVisible(False)  # Initially hidden
        question_layout.addWidget(answer_label)

        card_layout.addWidget(question_container)

        toggle_answer_button = QPushButton("Show Answer")
        toggle_answer_button.clicked.connect(lambda: self.toggle_answer(answer_label, toggle_answer_button))
        card_layout.addWidget(toggle_answer_button)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        card_layout.addWidget(line)

        button_layout = QHBoxLayout()

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_flashcard(flashcard))
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_flashcard(flashcard))
        button_layout.addWidget(delete_button)

        card_layout.addLayout(button_layout)

        # ✨ Apply the current theme colors
        self.style_flashcard(card_widget, question_container, toggle_answer_button, edit_button, delete_button, line)

        # 🌟 Save for dynamic theme refreshing
        if not hasattr(self, 'flashcard_widgets'):
            self.flashcard_widgets = []
        self.flashcard_widgets.append((card_widget, question_container, toggle_answer_button, edit_button, delete_button, line))

        return card_widget

    def toggle_answer(self, answer_label, toggle_button):
        if answer_label.isVisible():
            answer_label.setVisible(False)
            toggle_button.setText("Show Answer")
        else:
            answer_label.setVisible(True)
            toggle_button.setText("Hide Answer")

    def add_flashcard(self):
        self.editor = FlashcardEditor(self.user_id)
        if self.cached_theme:
            self.editor.apply_theme(self.cached_theme)
        self.editor.show()
        self.editor.saved.connect(self.load_flashcards)

    def edit_flashcard(self, flashcard):
        self.editor = FlashcardEditor(self.user_id, flashcard)
        if self.cached_theme:
            self.editor.apply_theme(self.cached_theme)
        self.editor.show()
        self.editor.saved.connect(self.load_flashcards)

    def delete_flashcard(self, flashcard):
        confirmation = QMessageBox.question(
            self, "Delete Flashcard",
            f"Are you sure you want to delete this flashcard?\n\nQuestion: {flashcard['question']}",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            delete_flashcard(self.user_id, flashcard['id'])
            self.load_flashcards()

    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        if theme:
            self.cached_theme = theme
            _, self.color_1, self.color_2, self.color_3, self.color_4 = theme.values()
        
    def apply_theme(self, theme):
        self.setStyleSheet(f"QWidget {{ background-color: {self.color_3}; }}")
        self.subject_dropdown.setStyleSheet(
            f"QComboBox {{ background-color: {self.color_2}; color: white; font-size: 14px; padding: 5px; border-radius: 5px; }}"
            f"QComboBox QAbstractItemView {{ background-color: {self.color_2}; color: white; selection-background-color: {self.color_3}; }}"
        )
        self.add_flashcard_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.color_2}; color: white; font-size: 18px; border-radius: 10px; padding: 10px; }}"
            f"QPushButton:hover {{ background-color: {self.color_3}; }}"
        )

        if hasattr(self, 'editor') and self.editor:
            self.editor.apply_theme(theme)

    def style_flashcard(self, card_widget, question_container, toggle_answer_button, edit_button, delete_button, line):
        card_widget.setStyleSheet(
            f"QWidget {{ background-color: {self.color_2}; border-radius: 10px; padding: 10px; }}"
        )
        question_container.setStyleSheet(
            f"QFrame {{ background-color: {self.color_4}; border-radius: 10px; border: 2px solid {self.color_1}; }}"
        )
        toggle_answer_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.color_4}; color: white; font-size: 16px; font-weight: bold; padding: 10px; border-radius: 5px; border: 2px solid {self.color_1}; }}"
            f"QPushButton:hover {{ background-color: {self.color_1}; }}"
        )
        edit_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.color_4}; color: white; font-weight: bold; padding: 10px; border-radius: 5px; border: 2px solid {self.color_1}; }}"
            f"QPushButton:hover {{ background-color: {self.color_1}; }}"
        )
        delete_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.color_4}; color: white; font-weight: bold; padding: 10px; border-radius: 5px; border: 2px solid {self.color_1}; }}"
            f"QPushButton:hover {{ background-color: {self.color_1}; }}"
        )
        line.setStyleSheet(f"background-color: {self.color_4}; height: 2px;")

    def refresh_theme(self):
        self.load_user_theme()
        self.apply_theme(self.cached_theme)

        # Restyle all flashcards
        if hasattr(self, 'flashcard_widgets'):
            for widgets in self.flashcard_widgets:
                if len(widgets) == 6:
                    card_widget, question_container, toggle_answer_button, edit_button, delete_button, line = widgets
                    self.style_flashcard(card_widget, question_container, toggle_answer_button, edit_button, delete_button, line)

        # Optional: Force a re-polish
        self.setStyle(QApplication.style())
        self.style().polish(self)
        self.update()

class FlashcardEditor(QWidget):
    saved = pyqtSignal()  # Signal to refresh flashcards after saving

    def __init__(self, user_id, flashcard=None):
        super().__init__()
        self.user_id = user_id
        self.flashcard = flashcard
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit Flashcard" if self.flashcard else "Add Flashcard")
        self.setGeometry(400, 200, 500, 400)

        layout = QVBoxLayout()

        # Subject Dropdown
        self.subject_dropdown = QComboBox()

        layout.addWidget(QLabel("Subject:"))
        layout.addWidget(self.subject_dropdown)
        self.load_subjects()

        # Question Input
        layout.addWidget(QLabel("Question:"))
        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText("Enter the question here...")
        layout.addWidget(self.question_input)

        # Answer Input
        layout.addWidget(QLabel("Answer:"))
        self.answer_input = QTextEdit()
        self.answer_input.setPlaceholderText("Enter the answer here...")
        layout.addWidget(self.answer_input)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_flashcard)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        if self.flashcard:
            self.load_existing_data()

    def apply_theme(self, theme):
        if not theme:
            return
        _, color_1, color_2, color_3, color_4 = theme.values()
        
        self.setStyleSheet(f"QWidget {{ background-color: {color_3}; }}")

        self.subject_dropdown.setStyleSheet(
            f"QComboBox {{ background-color: {color_2}; color: white; padding: 5px; border-radius: 5px; }}"
            f"QComboBox QAbstractItemView {{ background-color: {color_2}; color: white; }}"
        )

        self.save_button.setStyleSheet(
            f"QPushButton {{ background-color: {color_4}; color: white; padding: 10px; border-radius: 5px; }}"
            f"QPushButton:hover {{ background-color: {color_1}; }}"
        )

    def load_subjects(self):
        subjects = get_subjects(user_id=self.user_id)
        for subject in subjects:
            self.subject_dropdown.addItem(subject['name'], subject['id'])

        # If editing, pre-select the correct subject
        if self.flashcard:
            index = self.subject_dropdown.findData(self.flashcard['subject_id'])
            if index >= 0:
                self.subject_dropdown.setCurrentIndex(index)

    def load_existing_data(self):
        """ Load flashcard data into fields if editing. """
        self.question_input.setText(self.flashcard['question'])
        self.answer_input.setText(self.flashcard['answer'])

    def save_flashcard(self):
        """ Saves a new or updated flashcard. """
        question = self.question_input.toPlainText().strip()
        answer = self.answer_input.toPlainText().strip()
        subject_id = self.subject_dropdown.currentData()

        if not question or not answer:
            QMessageBox.warning(self, "Missing Fields", "Please fill out both the question and answer fields.")
            return

        if self.flashcard:
            update_flashcard(self.user_id, self.flashcard['id'], question, answer)
        else:
            add_flashcard(self.user_id, subject_id, question, answer)

        self.saved.emit()  # Notify the main app to refresh
        self.close()