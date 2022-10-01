#!python3.8

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QAbstractItemModel

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
            select_btn.clicked.connect(self.makeShowScore(calc.calc_score_for_test(test_plan_list, word)))
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

        # FormLayout中で文字列を入力する欄があった場合、その文字列からデータを引き抜く
        for i in reversed(range(layout.rowCount())):
            try:                
                label = layout.itemAt(i, layout.ItemRole(0)).widget()
            except AttributeError:
                label = None
            field = layout.itemAt(i, layout.ItemRole(1)).widget()
            # ラベル名に"名前"が含まれている場合、名前入力欄とし、フィールドから文字列を取り出す
            if type(label) == QLabel and "名前" in label.text() and type(field) == QLineEdit:
                players_name[f"player{len(players_name) + 1}"] = field.text()
        
        self.w.close()

        new_window = SingleGameWindow(players_name)
        new_window.show()
        

    def show(self):
        self.w.exec()

class SingleGameWindow(QWidget):
    def __init__(self, players:dict):
        
        self.players = players      # プレイヤー名格納
        self.tasks = []             # タスク格納
        self.sentences = {}         # 各プレイヤーの提示した文章格納{player_name:sentences}

        self.w = QDialog()
        self.w.resize(1280,720)
        self.w.setLayout(QVBoxLayout())
        
        self.createGameLayout()

    def createGameLayout(self):
        # 遷移部分
        game_preview = QStackedWidget()

        # Widgetをスタックさせる
        task_set_widget = QWidget()
        game_preview.addWidget(task_set_widget)
        input_widget = QWidget()
        game_preview.addWidget(input_widget)
        rank_widget = QWidget()
        game_preview.addWidget(rank_widget)

        # 遷移1 : タスク一覧設定
        task_set_layout = QFormLayout()
        task_set_widget.setLayout(task_set_layout)

        task_set_layout.addRow(QLabel("タスクを設定..."))
        task_count = QSpinBox()
        task_count.setMinimum(1)
        task_count.valueChanged.connect(lambda: self.createTaskInputSetting(task_count, task_set_layout))
        task_set_layout.addRow("タスク数:", task_count)

        task_set_layout.addRow("タスク1つ目", QLineEdit())
        
        task_set_button = QPushButton("タスクを設定する")
        task_set_button.clicked.connect(lambda:game_preview.setCurrentIndex(1))
        task_set_button.clicked.connect(lambda:self.setTaskList(task_set_layout))
        task_set_layout.addRow(task_set_button)

        # 遷移2 : 入力待機
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)

        input_layout.addWidget(QLabel("あなたが思う重要視すべき事柄はなにか入力しよう"))
        input_button = QPushButton("結果表示へ")
        input_button.clicked.connect(lambda:game_preview.setCurrentIndex(2))
        input_button.clicked.connect(lambda:self.setSentenceDict(players_layout))
        input_layout.addWidget(input_button)

        # 遷移3 : 結果表示
        rank_layout = QVBoxLayout()
        rank_widget.setLayout(rank_layout)
        rank_layout.addWidget(QLabel("☆結果発表☆"))
        calc_button = QPushButton("結果を表示する")
        calc_button.clicked.connect(lambda:self.setRankingView(rank_layout, calc_button))
        rank_layout.addWidget(calc_button)

        # 画面遷移する部分をウィンドウレイアウトに仕込む
        self.w.layout().addWidget(game_preview)

        # 固定部分(プレイヤー表示部)
        players_layout = QGridLayout()
        for i in range(len(self.players)):
            column_layout = QVBoxLayout()

            player_label = QLabel(list(self.players.keys())[i] + " : " + list(self.players.values())[i])
            player_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            column_layout.addWidget(player_label)
            
            player_input = QLineEdit()
            player_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            column_layout.addWidget(player_input)

            players_layout.addLayout(column_layout, int(i / 5), i % 5)
        
        self.w.layout().addLayout(players_layout)

    def setTaskList(self, layout:QFormLayout):
        for i in range(layout.count()):
            if layout.itemAt(i, layout.ItemRole(1)) and type(layout.itemAt(i, layout.ItemRole(1)).widget()) == QLineEdit:
                self.tasks.append(layout.itemAt(i, layout.ItemRole(1)).widget().text())
    
    def setSentenceDict(self, layout:QGridLayout):
        for i in range(layout.rowCount()):
            for j in range(layout.columnCount()):
                column = layout.itemAtPosition(i, j)
                if column is not None:self.sentences[f"{column.itemAt(0).widget().text()}"] = column.itemAt(1).widget().text()
    
    def setRankingView(self, layout, button:QPushButton):
        ranking_dict = {}
        rank_layout = QVBoxLayout()

        for sentence in self.sentences.items():
            for task in self.tasks:
                ranking_dict[f"{sentence[0]} {(task, sentence[1])}"] = calc.calc_score(task, sentence[1])

        sorted_rank_dict = sorted(ranking_dict.items(), key = lambda p : p[1], reverse=True)

        for p, ans in sorted_rank_dict:
            label = f"{rank_layout.count()+1}位 {p} {ans}点"
            rank_layout.addWidget(QLabel(label))
            if rank_layout.count() > 4: pass
        
        layout.addLayout(rank_layout)
        button.close()

    def createTaskInputSetting(self, task_count: QSpinBox, layout: QFormLayout):
        # 設定されたタスク数
        count = task_count.value()
        # 現在のタスクの入力欄数
        now_count = len([layout.itemAt(i, layout.ItemRole(1)) for i in range(layout.count()) if layout.itemAt(i, layout.ItemRole(0)) and "目" in layout.itemAt(i, layout.ItemRole(0)).widget().text()])

        if now_count < count:
            for _ in range(count - now_count):
                task_setting = QLineEdit()
                layout.insertRow(layout.rowCount() - 1, f"タスク{layout.rowCount() - 2}つ目:",task_setting)
        elif now_count > count:
            for _ in range(now_count - count):
                layout.removeRow(layout.rowCount() - 2)

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