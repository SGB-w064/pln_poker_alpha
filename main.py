#!python3.8

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
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

def createWindow():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

def main():
    createWindow()

if __name__ == "__main__":
    main()