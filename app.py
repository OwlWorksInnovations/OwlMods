import sys
import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QListWidget

# Sub file imports
from utils import get_files_in_dir, backup_files_dir, delete_file, backup_file

mods_dir = os.path.join(os.environ["APPDATA"], ".minecraft", "mods")
backup_dir = 'backup'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.setWindowTitle("OwlMods")
        self.setFixedSize(800, 600)
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(50, 50, 50, 50)

        # List box
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.get_mods()

        backup_layout = QVBoxLayout()
        self.list_widget_backup = QListWidget()
        backup_layout.addWidget(self.list_widget_backup)
        self.get_backups()
        self.backup_mods()

        self.restore_button = QPushButton("Restore")
        self.restore_button.setFixedHeight(30)
        backup_layout.addWidget(self.restore_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedHeight(30)
        layout.addWidget(self.delete_button)

        self.restore_button.clicked.connect(self.restore_mod)
        self.delete_button.clicked.connect(self.delete_mod)

        layout.addLayout(backup_layout)
        widget.setLayout(layout)

    def get_mods(self):
        mods_path: list = get_files_in_dir(mods_dir)
        mods: list = []

        for mod in mods_path:
            mods.append(os.path.basename(mod))

        self.list_widget.clear()
        self.list_widget.addItems(mods)
        
    def get_backups(self):
        mods_backup_path: list = get_files_in_dir(backup_dir)
        mods: list = []

        for mod in mods_backup_path:
            mods.append(os.path.basename(mod))

        self.list_widget_backup.clear()
        self.list_widget_backup.addItems(mods)

    def backup_mods(self):
        backup_files_dir(mods_dir, backup_dir)
        
    def delete_mod(self):
        filename = self.list_widget.currentItem()
        if filename:
            delete_file(mods_dir, filename.text().strip())
        
        self.get_mods()

    def restore_mod(self):
        filename = self.list_widget_backup.currentItem()

        if filename:
            backup_file(backup_dir, mods_dir, filename.text().strip())

        self.get_mods()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()