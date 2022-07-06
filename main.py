#!python3.8

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDialog, QPushButton
from PyQt6.QtCore import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)
        self.setWindowTitle("Planning Poker")
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("test")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        sub_window_button = QPushButton("create\nsub window")
        sub_window_button.clicked.connect(self.createWindow)
        layout.addWidget(sub_window_button)

    def createWindow(self):
        new_window = SubWindow()
        new_window.show()

class SubWindow(QWidget):
    def __init__(self):
        self.w = QDialog()
        self.w.resize(960, 540)
        label = QLabel()
        label.setText("sub")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.w.setLayout(layout)

    def show(self):
        self.w.exec()

def createMainWindow():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

def main():
    createMainWindow()

if __name__ == "__main__":
    main()