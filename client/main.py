#!python3.8

from dataclasses import field
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

import calc

test_plan_list = {"難所" : 1, "簡単" : 5, "細かい" : 10}
test_words = {"早さ" : 6, "正確さ" : 9, "実現可能性" : 4, "困難" : 0}

# 最初のウィンドウ
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

        open_single_btn = QPushButton("Single start", self)
        open_single_btn.clicked.connect(self.createSingleGameWindow)
        layout.addWidget(open_single_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        open_calc_btn = QPushButton("Calculation start", self)
        open_calc_btn.clicked.connect(self.createCalcWindow)
        layout.addWidget(open_calc_btn,alignment=Qt.AlignmentFlag.AlignCenter)

    def createSingleGameWindow(self):
        new_window = SingleGameSettingWindow()
        new_window.show()

    def createCalcWindow(self):
        try:
            new_window = CalcWindow()
            new_window.show()
        except ConnectionRefusedError:
            new_window = ErrorWindow()
            new_window.show()
            

class CalcWindow(QWidget):
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

        # 選択できる単語を並べる
        for word, _ in test_words.items():
            select_btn = QPushButton(word)
            select_btn.clicked.connect(self.makeShowScore(calc.calc_score(test_plan_list, word)))
            select_word_list.addWidget(select_btn)

        # ボタンをレイアウトに追加
        layout.addLayout(select_word_list)

        # レイアウトをウィンドウにセットする
        self.w.setLayout(layout)

    def makeShowScore(self, score):
        def showScore():
            self.score_label.setText(score)
        return showScore

    def show(self):
        self.w.exec()

class ErrorWindow(QWidget):
    def __init__(self):
        self.w = QDialog()
        self.w.resize(200, 100)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Error!"))

        self.w.setLayout(layout)
    
    def show(self):
        self.w.exec()

class SingleGameSettingWindow(QWidget):
    def __init__(self):
        self.w = QDialog()
        self.createSettingLayout()
    
    # プレイ人数の設定
    def createSettingLayout(self):
        self.w.resize(200,100)
        layout = QFormLayout()

        # プレイ人数設定
        player_count = QSpinBox()
        player_count.setMinimum(1)
        # プレイ人数に応じて、プレイヤー名の設定数を変更する
        player_count.valueChanged.connect(lambda: self.createPlayerNameSetting(player_count, layout))
        layout.addRow("プレイ人数:", player_count)

        # プレイヤー名の設定
        player_name_setting = QLineEdit()
        layout.addRow(f"プレイヤー{layout.rowCount()}の名前:",player_name_setting)

        # ゲーム画面への遷移
        start_game_button = QPushButton("ゲーム開始")
        start_game_button.clicked.connect(lambda: self.startGame())
        layout.addRow(start_game_button)
        
        self.w.setLayout(layout)

    def createPlayerNameSetting(self, player_count: QSpinBox, layout: QFormLayout):
        # プレイヤー名設定
        
        # 設定されたプレイヤー数
        count = player_count.value()
        # 表示されているプレイヤー名の入力欄数
        now_count = layout.rowCount() - 2

        if now_count < count:
            for _ in range(count - now_count):
                player_name_setting = QLineEdit()
                layout.insertRow(layout.rowCount() - 1, f"プレイヤー{layout.rowCount() - 1}の名前:",player_name_setting)
        elif now_count > count:
            for _ in range(now_count - count):
                layout.removeRow(layout.rowCount() - 2)
    
    def startGame(self):
        # 設定したレイアウトを取得
        layout:QFormLayout = self.w.layout()
        # プレイヤー名を格納する辞書型
        players_name = {}

        # FormLayout中で文字列を入力する欄があった場合、その文字列からプレイヤー名を引き抜く
        for i in reversed(range(layout.rowCount())):
            try:                
                label = layout.itemAt(i, QFormLayout.ItemRole(0)).widget()
            except AttributeError:
                label = None
            field = layout.itemAt(i, QFormLayout.ItemRole(1)).widget()
            if type(label) == QLabel and "名前" in label.text() and type(field) == QLineEdit:
                players_name[f"player{len(players_name) + 1}"] = field.text()
        self.w.close()
        print(players_name)

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