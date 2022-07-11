#!python3.8

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize

import calc

test_plan_list = {"難所" : 1, "簡単" : 5, "細かい" : 10}
test_words = {"早さ" : 6, "正確さ" : 9, "実現可能性" : 4, "困難" : 0}

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)
        self.setWindowTitle("Planning Poker")
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("test")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(label)

        open_game_btn = QPushButton("start", self)
        open_game_btn.clicked.connect(self.createGameWindow)

    def createGameWindow(self):
        new_window = GameWindow()
        new_window.show()

class GameWindow(QWidget):
    def __init__(self):
        self.w = QDialog()
        self.w.resize(960, 540)

        # 全体のレイアウトを作成
        layout = QVBoxLayout()
        # スコアのラベルを作成し全体のレイアウトに追加
        self.score_label = QLabel("default")
        layout.addWidget(self.score_label)

        # 単語選択のボタンを並べるレイアウトを作成
        select_word_list = QHBoxLayout()

        for word, weight in test_words.items():
            select_btn = QPushButton(word)
            select_btn.clicked.connect(self.makeShowScore(calc.test_calc_score(weight, test_plan_list)))
            select_word_list.addWidget(select_btn)

        layout.addLayout(select_word_list)
        self.w.setLayout(layout)

    def makeShowScore(self, score):
        def showScore():
            self.score_label.setText(score)
        return showScore

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