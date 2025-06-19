import sys
import os
import mysql.connector
from datetime import date , timedelta, datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QCheckBox, QLabel, 
                             QDialog, QSpinBox, QFormLayout, QDialogButtonBox,QComboBox,QTableWidgetItem,QTableWidget,
                             QDateEdit, QFrame, QScrollArea, QMessageBox,
                             QInputDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor
from db2 import (get_subjects, add_subject,
                     delete_subject, complete_subject, update_subject, get_topics, add_topic,
                     delete_topic,update_topic, complete_topic, get_tasks, add_task, update_task,
                     delete_task, complete_task, get_user_theme)
from calendar_integrated import StudyPlanner

def apply_theme_to_dialog(dialog, theme):
    _, color_1, color_2, color_3, color_4 = theme.values()

    # Apply general dialog style
    dialog.setStyleSheet(f"""
        QDialog {{
            background-color: {color_4};
            color: {color_1};
        }}
        QLabel {{
            background-color: {color_3};
            color: {color_1};
            font-weight: bold;
        }}
        QLineEdit, QDateEdit {{
            background-color: {color_2};
            color: {color_1};
            border: 1px solid {color_3};
            padding: 4px;
        }}
        QDateEdit::drop-down {{
            background-color: {color_3};
            color: {color_1};
        }}
        QPushButton {{
            background-color: {color_1};
            color: {color_2};
            border-radius: 4px;
            padding: 6px;
        }}
        QPushButton:hover {{
            background-color: {color_3};
        }}
    """)

    # Apply calendar-specific style if QDateEdit exists
    # Search for all QDateEdit children and apply style to their calendars
    for date_edit in dialog.findChildren(QDateEdit):
        calendar_widget = date_edit.calendarWidget()
        if calendar_widget:
            calendar_widget.setStyleSheet(f"""
                QCalendarWidget QToolButton {{
                    background-color: {color_1};
                    color: {color_2};
                    font-weight: bold;
                }}
                QCalendarWidget QMenu {{
                    background-color: {color_3};
                    color: {color_1};
                }}
                QCalendarWidget QWidget {{
                    background-color: {color_4};
                }}
                QCalendarWidget QAbstractItemView {{
                    selection-background-color: {color_2};
                    background-color: {color_3};
                    color: {color_1};
                }}
            """)


class AddTopicDialog(QDialog):
    def __init__(self, user_id, theme, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Topic")
        self.setFixedSize(300, 250)
        self.user_id = user_id
        self.theme = theme

        app = QApplication.instance()
        layout = QVBoxLayout()
        
        # Dialog title
        title_label = QLabel("Add Topic")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Times New Roman", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        # Topic name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name topic")
        layout.addWidget(QLabel("Name topic"))
        layout.addWidget(self.name_input)
        
        # Date picker
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("DD-MM-YYYY (Date)"))
        layout.addWidget(self.date_edit)
        
        # Done button
        self.done_button = QPushButton("Done")
        self.done_button.clicked.connect(self.accept)
        layout.addWidget(self.done_button)
        
        self.setLayout(layout)
        apply_theme_to_dialog(self, self.theme)

    def get_data(self):
        name = self.name_input.text()
        date = self.date_edit.date().toPyDate()
        return name, date
    
class EditTopicDialog(QDialog):
    def __init__(self, topic_data, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Topic")
        self.setFixedSize(300, 250)
        self.user_id = user_id

        layout = QVBoxLayout()
        
        # Dialog Topic
        title_label = QLabel("Edit Topic")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Times New Roman", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        # Topic title input
        self.name_input = QLineEdit()
        self.name_input.setText(topic_data['name'])
        layout.addWidget(QLabel("Topic name"))
        layout.addWidget(self.name_input)
        
        # Date picker
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if topic_data.get('due_date'):
            try:
                if isinstance(topic_data['due_date'], str):
                    self.date_edit.setDate(QDate.fromString(topic_data['due_date'], "yyyy-MM-dd"))
                else:
                    self.date_edit.setDate(QDate(topic_data['due_date']))
            except:
                self.date_edit.setDate(QDate.currentDate())
        else:
            self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("DD-MM-YYYY (Date)"))
        layout.addWidget(self.date_edit)
        
        # Done button
        self.done_button = QPushButton("Save")
        self.done_button.clicked.connect(self.accept)
        layout.addWidget(self.done_button)
        
        self.setLayout(layout)
        self.load_user_theme()

    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        apply_theme_to_dialog(self, theme)
    
    def get_data(self):
        name = self.name_input.text()
        date = self.date_edit.date().toPyDate()
        return name, date

class AddTaskDialog(QDialog):
    def __init__(self, user_id, theme, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Task")
        self.setFixedSize(300, 250)
        self.user_id = user_id
        self.theme = theme

        layout = QVBoxLayout()
        
        # Dialog title
        title_label = QLabel("Add Task")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Times New Roman", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        # Task name input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Name task")
        layout.addWidget(QLabel("Name task"))
        layout.addWidget(self.title_input)
        
        # Date picker
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("DD-MM-YYYY (Date)"))
        layout.addWidget(self.date_edit)
        
        # Done button
        self.done_button = QPushButton("Done")
        self.done_button.clicked.connect(self.accept)
        layout.addWidget(self.done_button)
        
        self.setLayout(layout)
        apply_theme_to_dialog(self, self.theme)

    def get_data(self):
        title = self.title_input.text()
        date = self.date_edit.date().toPyDate()
        return title, date

class EditTaskDialog(QDialog):
    def __init__(self, task_data, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Task")
        self.setFixedSize(300, 250)
        self.user_id = user_id

        layout = QVBoxLayout()
        
        # Dialog title
        title_label = QLabel("Edit Task")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Times New Roman", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        # Task title input
        self.title_input = QLineEdit()
        self.title_input.setText(task_data['title'])
        layout.addWidget(QLabel("Task title"))
        layout.addWidget(self.title_input)
        
        # Date picker
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if task_data.get('due_date'):
            try:
                if isinstance(task_data['due_date'], str):
                    self.date_edit.setDate(QDate.fromString(task_data['due_date'], "yyyy-MM-dd"))
                else:
                    self.date_edit.setDate(QDate(task_data['due_date']))
            except:
                self.date_edit.setDate(QDate.currentDate())
        else:
            self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("DD-MM-YYYY (Date)"))
        layout.addWidget(self.date_edit)
        
        # Done button
        self.done_button = QPushButton("Save")
        self.done_button.clicked.connect(self.accept)
        layout.addWidget(self.done_button)
        
        self.setLayout(layout)
        self.load_user_theme()

    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        apply_theme_to_dialog(self, theme)

    def get_data(self):
        title = self.title_input.text()
        date = self.date_edit.date().toPyDate()
        return title, date

class TaskItem(QWidget):
    def __init__(self, task_data, user_id, subject_id, theme, parent=None, topic_id=None):
        super().__init__(parent)
        self.task_data = task_data
        self.user_id = user_id
        self.subject_id = subject_id
        self.topic_id = topic_id
        self.task_id = task_data['id']
        self.title = task_data['title']
        self.status = task_data.get('status', 'Pending')
        self.due_date = task_data.get('due_date')
        self.parent_widget = parent

        self.theme = theme

        self.init_ui()
        self.apply_theme(self.theme)

    def apply_theme(self, theme):
        _, self.color_1, self.color_2, self.color_3, self.color_4 = theme.values()

        self.checkbox.setStyleSheet(f"""
            QCheckBox::indicator:checked {{ background-color: {self.color_1}; }}
        """)
        
        if self.status == 'Completed':
            self.title_label.setStyleSheet(f"text-decoration: line-through; color: {self.color_1};")
        else:
            self.title_label.setStyleSheet(f"color: {self.color_1};")
        
        self.edit_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_4}; color: white; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_1}; }}
        """)
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_3}; color: {self.color_2}; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_4}; color: {self.color_2} }}
        """)
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.status == 'Completed')
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        
        # Task title
        self.title_label = QLabel(self.title)
        
        # Edit and Delete buttons
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.edit_task)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_task)
       
        layout.addWidget(self.checkbox)
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)
        
        self.setLayout(layout)

    def on_checkbox_changed(self, state):
        try:
            is_checked = (state == Qt.Checked)
            if is_checked:
                result = complete_task(self.user_id, self.subject_id, self.task_id, self.topic_id)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not update task: {str(result)}")
                    self.checkbox.setChecked(False)
                    return

                self.status = 'Completed'
                self.apply_theme(self.theme)
                self.check_parent_completion()
            else:
                # Prevent unchecking if not allowed
                self.checkbox.setChecked(True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
            self.checkbox.setChecked(True)
    
    def check_parent_completion(self):
        # Check if this task belongs to a topic or directly to a subject
        if self.topic_id:
            # Get the parent topic widget
            parent_widget = self.parent_widget
            if parent_widget and hasattr(parent_widget, 'check_all_tasks_completed'):
                parent_widget.check_all_tasks_completed()
        else:
            # Get the parent subject widget
            parent_widget = self.parent_widget
            if parent_widget and hasattr(parent_widget, 'check_all_completed'):
                parent_widget.check_all_completed()
    
    def edit_task(self):
        try:
            dialog = EditTaskDialog(self.task_data, self.user_id, self)
            if dialog.exec_() == QDialog.Accepted:
                title, date = dialog.get_data()
                if not title:
                    QMessageBox.warning(self, "Input Required", "Please enter a task title")
                    return
                
                result = update_task(self.user_id, self.subject_id, self.task_id, title, date)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not update task: {str(result)}")
                    return
                
                self.title = title
                self.due_date = date
                self.title_label.setText(title)
                self.task_data['title'] = title
                self.task_data['due_date'] = date

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def delete_task(self):
        try:
            # Create a themed confirmation message box
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Delete Task")
            msg_box.setText(f"Are you sure you want to delete '{self.title}'?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)

            # Apply current theme colors
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {self.color_4};
                    color: {self.color_1};
                }}
                QLabel {{
                    background-color: {self.color_3};
                    color: {self.color_1};
                    font-weight: bold;
                }}
                QPushButton {{
                    background-color: {self.color_3};
                    color: {self.color_4};
                    border-radius: 4px;
                    padding: 6px;
                }}
                QPushButton:hover {{
                    background-color: {self.color_2};
                }}
            """)

            reply = msg_box.exec_()

            if reply == QMessageBox.Yes:
                result = delete_task(self.user_id, self.subject_id, self.task_id)
                if isinstance(result, Exception):
                    self.themed_message_box("Error", f"Could not delete task: {str(result)}", QMessageBox.Warning)
                    return

                # Remove from UI if parent allows
                if self.parent_widget and hasattr(self.parent_widget, 'remove_task'):
                    self.parent_widget.remove_task(self)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

class TopicItem(QWidget):
    def __init__(self, topic_data, user_id, subject_id, theme, parent=None):
        super().__init__(parent)
        self.topic_data = topic_data
        self.user_id = user_id
        self.subject_id = subject_id
        self.topic_id = topic_data['id']
        self.name = topic_data['name']
        self.status = topic_data.get('status', 'Pending')
        self.due_date = topic_data.get('due_date')
        self.tasks = []
        self.parent_widget = parent
        self.theme = theme

        self.init_ui()
        self.load_tasks()
        self.apply_theme(self.theme)

    def apply_theme(self, theme):
        _, self.color_1, self.color_2, self.color_3, self.color_4 = theme.values()
        self.checkbox.setStyleSheet(f"""
            QCheckBox::indicator:checked {{ background-color: {self.color_1}; }}
        """)

        if self.status == 'Completed':
            self.name_label.setStyleSheet(f"text-decoration: line-through; color: {self.color_1}; font-weight: bold;")
        else:
            self.name_label.setStyleSheet(f"color: {self.color_1}; font-weight: bold;")
        
        self.edit_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_4}; color: white; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_1}; }}
        """)
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_3}; color: {self.color_2}; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_4}; color: {self.color_2} }}
        """)
        self.add_task_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_1}; color: white; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_4}; }}
        """)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.status == 'Completed')
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        # Topic header
        header_layout = QHBoxLayout()    
        
        # Topic name
        self.name_label = QLabel(self.name)

        # Edit and Delete buttons
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.edit_topic)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_topic)
        
        # Add task button
        self.add_task_btn = QPushButton("Add task")
        self.add_task_btn.clicked.connect(self.add_task)
       
        header_layout.addWidget(self.checkbox)
        header_layout.addWidget(self.name_label)
        header_layout.addStretch()
        header_layout.addWidget(self.edit_btn)
        header_layout.addWidget(self.delete_btn)
        header_layout.addWidget(self.add_task_btn)
        
        # Tasks container
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setContentsMargins(20, 0, 0, 0)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.tasks_container)
        
        self.setLayout(layout)
        
    def on_checkbox_changed(self, state):
        is_checked = (state == Qt.Checked)
        if is_checked:
            complete_topic(self.user_id, self.subject_id, self.topic_id)
            self.status = 'Completed'
            self.apply_theme(self.theme)

            # Mark all tasks as completed
            for i in range(self.tasks_layout.count()):
                task_widget = self.tasks_layout.itemAt(i).widget()
                if task_widget and hasattr(task_widget, 'checkbox'):
                    task_widget.checkbox.setChecked(True)

            self.check_subject_completion()
        else:
            self.checkbox.setChecked(True)  # Prevent unchecking

    def check_subject_completion(self):
        # Get the parent subject widget
        subject_widget = self.parent_widget
        if subject_widget and hasattr(subject_widget, 'check_all_completed'):
            subject_widget.check_all_completed()
    
    def check_all_tasks_completed(self):
        all_completed = True
        
        # Check if all tasks are completed
        for i in range(self.tasks_layout.count()):
            task_widget = self.tasks_layout.itemAt(i).widget()
            if task_widget and hasattr(task_widget, 'status') and task_widget.status != 'Completed':
                all_completed = False
                break
        
        # If all tasks are completed, mark the topic as completed
        if all_completed and self.tasks_layout.count() > 0:
            self.checkbox.setChecked(True)
    
    def edit_topic(self):
        try:
            input_dialog = EditTopicDialog(self.topic_data, self.user_id, self)
            if input_dialog.exec_() == QDialog.Accepted:
                name, date = input_dialog.get_data()
                if not name:
                    QMessageBox.warning(self, "Input Required", "Please enter a topic name")
                    return
                    
                result = update_topic(self.user_id, self.subject_id, self.topic_id, name, date)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not update topic: {str(result)}")
                    return
                
                self.name = name
                self.due_date = date
                self.name_label.setText(name)
                self.topic_data['name'] = name
                self.topic_data['due_date'] = date

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def delete_topic(self):
        try:
            # Create a styled message box
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Delete Topic")
            msg_box.setText(f"Are you sure you want to delete '{self.name}'?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {self.color_4};
                    color: {self.color_1};
                    font-weight: bold;
                }}
                QLabel {{
                    background-color: {self.color_3};
                    color: {self.color_1};
                }}
                QPushButton {{
                    background-color: {self.color_3};
                    color: white;
                    border-radius: 4px;
                    padding: 6px;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: {self.color_2};
                }}
            """)
            
            reply = msg_box.exec_()
            
            if reply == QMessageBox.Yes:

                # Then delete the topic
                result = delete_topic(self.user_id, self.subject_id, self.topic_id)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not delete topic: {str(result)}")
                    return
                
                # Remove from UI
                if self.parent_widget and hasattr(self.parent_widget, 'remove_topic'):
                    self.parent_widget.remove_topic(self)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def add_task(self):
        try:
            # Show task dialog
            dialog = AddTaskDialog(self.user_id, self.theme, self)
            if dialog.exec_() == QDialog.Accepted:
                title, date = dialog.get_data()
                if not title:
                    QMessageBox.warning(self, "Input Required", "Please enter a task title")
                    return
                
                # Add task to the topic
                result = add_task(self.user_id, self.subject_id, title, date, self.topic_id)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not add task: {str(result)}")
                    return
                
                # Add the new task to UI
                task_item = TaskItem(result[0], self.user_id, self.subject_id, self.theme, self, self.topic_id)
                self.tasks.append(task_item)
                self.tasks_layout.addWidget(task_item)
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def add_task_to_ui(self, task_data):
        task_item = TaskItem(task_data, self.user_id, self.subject_id, self.theme, self)
        self.tasks.append(task_item)
        self.tasks_layout.addWidget(task_item)

    def remove_task(self, task_item):
        if task_item in self.tasks:
            self.tasks.remove(task_item)
            self.tasks_layout.removeWidget(task_item)
            task_item.deleteLater()
    
    def load_tasks(self):
        # Clear existing tasks
        while self.tasks_layout.count():
            item = self.tasks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.tasks.clear()
        
        # Get tasks for this topic
        tasks = get_tasks(self.user_id, self.subject_id, self.topic_id)
        if isinstance(tasks, Exception):
            QMessageBox.warning(self, "Error", f"Could not load tasks: {str(tasks)}")
            return
        
        for task_data in tasks:
            task_item = TaskItem(task_data, self.user_id, self.subject_id, self.theme, self, self.topic_id)
            self.tasks.append(task_item)
            self.tasks_layout.addWidget(task_item)

class SubjectItem(QFrame):
    def __init__(self, subject_data, user_id, theme, parent=None):
        super().__init__(parent)
        self.subject_data = subject_data
        self.user_id = user_id
        self.subject_id = subject_data['id']
        self.name = subject_data['name']
        self.status = subject_data.get('status', 'Pending')
        self.topics = []
        self.subject_tasks = []  # Direct tasks under subject
        self.parent_widget = parent
        self.theme = theme
        
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)

        self.init_ui()
        self.load_topics()
        self.load_subject_tasks()
        self.apply_theme(self.theme)

    def apply_theme(self, theme):
        _, self.color_1, self.color_2, self.color_3, self.color_4 = theme.values()
        self.setStyleSheet(f"""
            SubjectItem {{ 
                border: 1px solid {self.color_3};
                border-radius: 6px;
            }}
        """)
        self.checkbox.setStyleSheet(f"""
            QCheckBox::indicator:checked {{ background-color: {self.color_1}; }}
        """)
        self.subject_label.setStyleSheet(f"color: {self.color_1}; font-weight: bold;")

        if self.status == 'Completed':
            self.name_label.setStyleSheet(f"text-decoration: line-through; color: {self.color_1};")
        else:
            self.name_label.setStyleSheet(f"color: {self.color_1};")
        
        self.edit_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_4}; color: white; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_1}; }}
        """)
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_3}; color: {self.color_2}; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_4}; color: {self.color_2} }}
        """)
        self.add_task_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_1}; color: white; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_4}; }}
        """)
        self.add_topic_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.color_1}; color: white; border-radius: 4px; padding: 4px 8px; }}
            QPushButton:hover {{ background-color: {self.color_4}; }}
        """)

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Subject header
        header_layout = QHBoxLayout()
        
        # Subject checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.status == 'Completed')
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
            
        self.subject_label = QLabel()
            
        self.name_label = QLabel(self.name)
        self.name_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        
        # Edit and Delete buttons
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.edit_subject)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_subject)
        
        # Add task and topic buttons
        self.add_task_btn = QPushButton("Add task")
        self.add_task_btn.clicked.connect(self.add_task)
        
        self.add_topic_btn = QPushButton("Add topic")
        self.add_topic_btn.clicked.connect(self.add_topic)
        
        header_layout.addWidget(self.checkbox)
        header_layout.addWidget(self.subject_label)
        header_layout.addWidget(self.name_label)
        header_layout.addStretch()
        header_layout.addWidget(self.edit_btn)
        header_layout.addWidget(self.delete_btn)
        header_layout.addWidget(self.add_task_btn)
        header_layout.addWidget(self.add_topic_btn)

        # Subject-level tasks container
        self.subject_tasks_container = QWidget()
        self.subject_tasks_layout = QVBoxLayout(self.subject_tasks_container)
        self.subject_tasks_layout.setContentsMargins(20, 0, 0, 0)

        self.topics_container = QWidget()
        self.topics_layout = QVBoxLayout(self.topics_container)
        self.topics_layout.setContentsMargins(20, 0, 0, 0)
        
        #header_layout.addWidget(self.checkbox)
        layout.addLayout(header_layout)
        layout.addWidget(self.subject_tasks_container)
        layout.addWidget(self.topics_container)
        
        self.setLayout(layout)
        
    def on_checkbox_changed(self, state):
        is_checked = (state == Qt.Checked)
        if not is_checked:
            self.checkbox.setChecked(True)  # Prevent unchecking
            return

        complete_subject(self.user_id, self.subject_id)
        self.status = 'Completed'
        self.apply_theme(self.theme)

        # Mark all direct tasks as completed
        for i in range(self.subject_tasks_layout.count()):
            task_widget = self.subject_tasks_layout.itemAt(i).widget()
            if task_widget and hasattr(task_widget, 'checkbox'):
                task_widget.checkbox.setChecked(True)

        # Mark all topics (and their tasks) as completed
        for i in range(self.topics_layout.count()):
            topic_widget = self.topics_layout.itemAt(i).widget()
            if topic_widget and hasattr(topic_widget, 'checkbox'):
                topic_widget.checkbox.setChecked(True)

        self.checkbox.setDisabled(True)  # Prevent further interaction

    def check_all_completed(self):
        all_completed = True
        
        # Check if all topics are completed
        for i in range(self.topics_layout.count()):
            topic_widget = self.topics_layout.itemAt(i).widget()
            if topic_widget and hasattr(topic_widget, 'status') and topic_widget.status != 'Completed':
                all_completed = False
                break
        
        # Check if all direct tasks are completed
        for i in range(self.subject_tasks_layout.count()):
            task_widget = self.subject_tasks_layout.itemAt(i).widget()
            if task_widget and hasattr(task_widget, 'status') and task_widget.status != 'Completed':
                all_completed = False
                break
        
        # If all topics and tasks are completed, mark the subject as completed
        if all_completed and (self.topics_layout.count() > 0 or self.subject_tasks_layout.count() > 0):
            self.checkbox.setChecked(True)
    
    def edit_subject(self):
    #   self.load_user_theme()
        try:
            # Create a styled input dialog
            input_dialog = QInputDialog(self)
            input_dialog.setWindowTitle("Edit Subject")
            input_dialog.setLabelText("Enter new subject name:")
            input_dialog.setTextValue(self.name)
            input_dialog.setStyleSheet(f"""
                QInputDialog {{
                    background-color: {self.color_3};
                    color: {self.color_1};
                }}
                QLabel {{
                    color: {self.color_1};
                    background-color: {self.color_3};
                }}
                QLineEdit {{
                    background-color: white;
                    color: black;
                    border: 1px solid {self.color_1};
                    border-radius: 4px;
                    padding: 4px;
                }}
                QPushButton {{
                    background-color: {self.color_1};
                    color: white;
                    border-radius: 4px;
                    padding: 6px;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: {self.color_4};
                }}
            """)
            
            ok = input_dialog.exec_()
            name = input_dialog.textValue()
            
            if ok and name:
                result = update_subject(self.user_id, self.subject_id, name)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not update subject: {str(result)}")
                    return
                
                self.name = name
                self.name_label.setText(name)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def delete_subject(self):
        try:
            # Create a styled message box
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Delete Subject")
            msg_box.setText(f"Are you sure you want to delete '{self.name}'?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color:{self.color_4};
                    color: {self.color_1};
                }}
                QLabel {{
                    color: {self.color_1};
                }}
                QPushButton {{
                    background-color: {self.color_1};
                    color: white;
                    border-radius: 4px;
                    padding: 6px;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: {self.color_2};
                }}
            """)
            
            reply = msg_box.exec_()
            
            if reply == QMessageBox.Yes:
                result = delete_subject(self.user_id, self.subject_id)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not delete subject: {str(result)}")
                    return
                
                # Remove from UI
                if self.parent_widget and hasattr(self.parent_widget, 'remove_subject'):
                    self.parent_widget.remove_subject(self)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def add_topic(self):
        try:
            dialog = AddTopicDialog(self.user_id, self.theme, self)
            if dialog.exec_() == QDialog.Accepted:
                name, date = dialog.get_data()
                if not name:
                    QMessageBox.warning(self, "Input Required", "Please enter a topic name")
                    return
                
                result = add_topic(self.user_id, self.subject_id, name, date)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not add topic: {str(result)}")
                    return
                
                topic_item = self.add_topic_to_ui(result[0])

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        
    def add_task(self):
        try:
            # Show task dialog
            dialog = AddTaskDialog(self.user_id, self.theme, self)
            if dialog.exec_() == QDialog.Accepted:
                title, date = dialog.get_data()
                if not title:
                    QMessageBox.warning(self, "Input Required", "Please enter a task title")
                    return
                
                # Add task directly to the subject using the existing add_task function
                result = add_task(self.user_id, self.subject_id, title, date)
                if isinstance(result, Exception):
                    QMessageBox.warning(self, "Error", f"Could not add task: {str(result)}")
                    return
                task_item = self.add_task_to_ui(result[0])

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def add_task_to_ui(self, task_data):
        task_item = TaskItem(task_data, self.user_id, self.subject_id, self.theme, self)
        self.subject_tasks.append(task_item)
        self.subject_tasks_layout.addWidget(task_item)
    
    def add_topic_to_ui(self, topic_data):
        topic_item = TopicItem(topic_data, self.user_id, self.subject_id, self.theme, self)
        self.topics.append(topic_item)
        self.topics_layout.addWidget(topic_item)
        return topic_item
    
    def remove_topic(self, topic_item):
        if topic_item in self.topics:
            self.topics.remove(topic_item)
            self.topics_layout.removeWidget(topic_item)
            topic_item.deleteLater()
            
            # Check if all remaining topics and tasks are completed
            self.check_all_completed()
    
    def remove_task(self, task_item):
        if task_item in self.subject_tasks:
            self.subject_tasks.remove(task_item)
            self.subject_tasks_layout.removeWidget(task_item)
            task_item.deleteLater()
            
            # Check if all remaining topics and tasks are completed
            self.check_all_completed()
    
    def load_topics(self):
        # Clear existing topics
        while self.topics_layout.count():
            item = self.topics_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        #self.topics = []
        self.topics.clear()
        
        # Get topics for this subject
        topics = get_topics(self.user_id, self.subject_id)
        if isinstance(topics, Exception):
            QMessageBox.warning(self, "Error", f"Could not load topics: {str(topics)}")
            return
        
        for topic_data in topics:
            self.add_topic_to_ui(topic_data)
    
    def load_subject_tasks(self):
        # Clear existing tasks
        while self.subject_tasks_layout.count():
            item = self.subject_tasks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.subject_tasks = []
        
        # Get tasks directly under this subject (not in any topic)
        tasks = get_tasks(self.user_id, self.subject_id)
        if isinstance(tasks, Exception):
            QMessageBox.warning(self, "Error", f"Could not load subject tasks: {str(tasks)}")
            return
        
        for task_data in tasks:
            self.add_task_to_ui(task_data)

class TodoList(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.subjects = []
    #   self.task_items = []
        self.load_user_theme()
        self.init_ui()
        self.load_subjects()
        self.apply_theme()
    
    def refresh_theme(self):
        self.load_user_theme()
        self.apply_theme()
        
        for subject_item in self.subjects:
            subject_item.theme = self.theme  # Pass reference to updated theme
            subject_item.apply_theme(self.theme)
            for task in getattr(subject_item, 'subject_tasks', []):
                task.theme = self.theme  # Update theme reference
                task.apply_theme(self.theme)
            for topic in getattr(subject_item, 'topics', []):
                topic.theme = self.theme  # Update theme reference
                topic.apply_theme(self.theme)
                for task in getattr(topic, 'tasks', []):
                    task.theme = self.theme  # Update theme reference
                    task.apply_theme(self.theme)

    def load_user_theme(self):
        self.theme = get_user_theme(self.user_id)
        _, self.color_1, self.color_2, self.color_3, self.color_4 = self.theme.values()

    def apply_theme(self):
        self.setStyleSheet(f"""
            QWidget {{ background-color: {self.color_2}; }}
            QLabel {{ color: {self.color_1}; }}
            QLineEdit {{ background-color: white; color: black; border: 1px solid {self.color_1}; border-radius: 4px; padding: 4px; }}
            QPushButton {{ background-color: {self.color_1}; color: white; border-radius: 4px; padding: 6px; }}
            QPushButton:hover {{ background-color: {self.color_3}; }}
            QMessageBox {{ background-color: {self.color_3}; color: {self.color_1}; }}
            QInputDialog {{ background-color: {self.color_3}; color: {self.color_1}; }}
        """)
        
        self.title_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.color_3};
                color: {self.color_2};
                border: 3px solid {self.color_1};
                border-radius: 6px;
            }}
        """)

        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {self.color_4}; 
                border: 1px solid {self.color_1};
                border-radius: 6px;
            }}
        """)

        self.subjects_container.setStyleSheet(f"background-color: {self.color_2};")

    def init_ui(self):
        self.setWindowTitle("To-Do List")
        self.resize(800, 600)
        
        main_layout = QVBoxLayout()
        
        # Title
        self.title_label = QLabel("TO - DO - LIST")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Times New Roman", 16, QFont.Bold))
        self.title_label.setFrameShape(QFrame.Box)
        self.title_label.setFrameShadow(QFrame.Raised)
        self.title_label.setLineWidth(1)
        self.title_label.setFixedHeight(50)
        
        # Scroll area for subjects
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Box)
        self.scroll_area.setFrameShadow(QFrame.Raised)
        self.scroll_area.setLineWidth(1)
        
        self.subjects_container = QWidget()
        self.subjects_layout = QVBoxLayout(self.subjects_container)
        self.subjects_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(self.subjects_container)
        self.calendar_button = QPushButton("View Calendar")
        self.calendar_button.clicked.connect(self.open_calendar)
        main_layout.addWidget(self.calendar_button)

        # Add subject area
        input_layout = QHBoxLayout()
        
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Add subject")
        
        self.add_button = QPushButton("Done")
        self.add_button.clicked.connect(self.add_subject)
        
        input_layout.addWidget(self.subject_input)
        input_layout.addWidget(self.add_button)
        
        # Add everything to main layout
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(input_layout)
        
        self.setLayout(main_layout)

    def add_subject(self):
        try:
            name = self.subject_input.text().strip()
            if not name:
                QMessageBox.warning(self, "Input Required", "Please enter a subject name")
                return
            
            result = add_subject(self.user_id, name)
            if isinstance(result, Exception):
                QMessageBox.warning(self, "Error", f"Could not add subject: {str(result)}")
                return
            
            self.subject_input.clear()
            self.add_subject_to_ui(result[0])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def add_subject_to_ui(self, subject_data):
        subject_item = SubjectItem(subject_data, self.user_id, self.theme, self)
        self.subjects.append(subject_item)
        self.subjects_layout.addWidget(subject_item)
        return subject_item
    
    def remove_subject(self, subject_item):
        if subject_item in self.subjects:
            self.subjects.remove(subject_item)
            self.subjects_layout.removeWidget(subject_item)
            subject_item.deleteLater()

    def get_all_due_dates(self):
        due_dates = set()
        for subject in self.subjects:
            for task in subject.subject_tasks:
             if task.due_date:
                due_dates.add(task.due_date)
            for topic in subject.topics:
             if topic.due_date:
                due_dates.add(topic.due_date)
            for task in topic.tasks:
                if task.due_date:
                    due_dates.add(task.due_date)
        return due_dates

    def open_calendar(self):
        self.calendar_window = StudyPlanner(self.user_id)
        task_data = []

    # Subject-level tasks
        for subject in self.subjects:
            for task in subject.subject_tasks:
                if task.due_date:
                  is_completed = (task.status == 'Completed')
                  task_data.append((task.due_date, task.title, is_completed))

        # Topic-level tasks + topics themselves
            for topic in subject.topics:
             if topic.due_date:
                is_completed = (topic.status == 'Completed')
                task_data.append((topic.due_date, f"Topic: {topic.name}", is_completed))

             for task in topic.tasks:
                if task.due_date:
                    is_completed = (task.status == 'Completed')
                    task_data.append((task.due_date, task.title, is_completed))

        self.calendar_window.set_task_data(task_data)
        self.calendar_window.show()    

    def load_subjects(self):
        # Clear existing subjects
        while self.subjects_layout.count():
            item = self.subjects_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        #self.subjects = []
        self.subjects.clear()
        
        # Get subjects for this user
        subjects = get_subjects(self.user_id)
        if isinstance(subjects, Exception):
            QMessageBox.warning(self, "Error", f"Could not load subjects: {str(subjects)}")
            return
        
        for subject_data in subjects:
            self.add_subject_to_ui(subject_data)