import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QHeaderView
from PyQt5.QtCore import Qt
import sys
from db2 import get_app, get_panels, get_resources, get_developers, get_user_theme

class AboutPage(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.load_user_theme()
        self.setWindowTitle("About the App")
        self.setGeometry(100, 100, 800, 500)  # Increased size to fit 3 columns
        # Set up the main layout with a vertical box layout
        main_layout = QVBoxLayout()

        # App Name label, centered
        self.app_name_label = QLabel("App Name")
        self.app_name_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.app_name_label)

        # Set up horizontal layout for three columns: Developers, Panels, Resources
        horizontal_layout = QHBoxLayout()

        # Create TreeWidget for Developers, Panels, Resources
        self.dev_tree = QTreeWidget()
        self.panels_tree = QTreeWidget()
        self.resources_tree = QTreeWidget()

        # Add trees to the horizontal layout
        horizontal_layout.addWidget(self.dev_tree)
        horizontal_layout.addWidget(self.panels_tree)
        horizontal_layout.addWidget(self.resources_tree)

        # Apply theme and styles to all components
        self.apply_theme()

        # Populate the trees
        self.populate_tree()

        # Add horizontal layout to the main layout
        main_layout.addLayout(horizontal_layout)

        # Set the final layout
        self.setLayout(main_layout)

    def load_user_theme(self):
        theme = get_user_theme(self.user_id)
        if theme:
            _, self.color_1, self.color_2, self.color_3, self.color_4 = theme.values()

    def apply_theme(self):
        self.setStyleSheet(f"background-color: {self.color_3};")
        self.app_name_label.setStyleSheet(f"""
            font-size: 35px;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            color: {self.color_1};
            padding: 20px;
        """)
        
        # Apply style to all tree widgets
        for tree in [self.dev_tree, self.panels_tree, self.resources_tree]:
            self._set_tree_style(tree)

    def refresh_theme(self):
        self.load_user_theme()
        self.apply_theme()

    def _set_tree_style(self, tree_widget):
        tree_widget.setHeaderHidden(True)
        tree_widget.setColumnCount(1)  # 1 visible column
        tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        tree_widget.header().setStretchLastSection(False)
        tree_widget.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {self.color_2};
                border: 1px solid {self.color_1};
                border-radius: 8px;
                padding: 8px;
                font-size: 17px;
            }}
            QTreeWidget::item {{
                height: 28px;
                padding-left: 6px;
                padding-right: 6px;
                margin: 6px;
                background-color: {self.color_4};
                color: {self.color_1};
            }}
            QTreeWidget::item:hover {{
                background-color: {self.color_4};
            }}
        """)

    def populate_tree(self):
        # Get app info and populate the trees
        app = get_app()
        app_name = app['name']

        # Set the app name in the label
        self.app_name_label.setText(app_name)

        # Developers
        developers = get_developers()
        dev_root = QTreeWidgetItem(["Developers"])
        self.dev_tree.addTopLevelItem(dev_root)
        dev_root.setExpanded(True)
        for dev in developers:
            name_with_role = f"{dev['name']} ({dev['role_name']})"
            dev_item = QTreeWidgetItem([name_with_role])
            dev_root.addChild(dev_item)

            # Set tooltips for developer item
            dev_item.setToolTip(0, f"Email: {dev['email']}\nRole: {dev['description']}")

        # Panels
        panels = get_panels(app['id'])
        panels_root = QTreeWidgetItem(["Panels"])
        self.panels_tree.addTopLevelItem(panels_root)
        panels_root.setExpanded(True)
        for panel in panels:
            panel_item = QTreeWidgetItem([panel['name']])
            panels_root.addChild(panel_item)

            # Set tooltip for panel item
            panel_item.setToolTip(0, f"Description: {panel['description']}")

        # Resources
        resources = get_resources(app['id'])
        resources_root = QTreeWidgetItem(["Resources"])
        self.resources_tree.addTopLevelItem(resources_root)
        resources_root.setExpanded(True)
        for res in resources:
            res_item = QTreeWidgetItem([res['name']])
            resources_root.addChild(res_item)

            # Set tooltip for resource item
            res_item.setToolTip(0, f"Description: {res['description']}")