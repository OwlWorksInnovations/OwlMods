import sys
import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QListWidget

# Sub file imports
from utils import get_files_in_dir, backup_files_dir

mods_dir = os.path.join(os.environ["APPDATA"], ".minecraft", "mods")

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

        widget.setLayout(layout)

    def get_mods(self):
        mods_path: list = get_files_in_dir(mods_dir)
        mods: list = []

        for mod in mods_path:
            mods.append(os.path.basename(mod))
        
        self.list_widget.addItems(mods)

        self.backup_mods()

    def backup_mods(self):
        try:
            backup_files_dir(mods_dir, "./backup")
        except FileExistsError:
            print("File exists")
            return

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()