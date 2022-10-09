#python3.8

from ctypes import alignment
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

import calc

class SingleGameSettingWindow(QWidget):
    def __init__(self):
        self.w = QDialog()
        self.createSettingLayout()
    
    # プレイ人数の設定
    def createSettingLayout(self):
        self.w.resize(200,100)
        # 画面のレイアウト設定
        layout = QFormLayout()
        # プレイヤー名の入力フォームのレイアウト
        name_input_layout = QFormLayout()

        # プレイ人数設定
        player_count = QSpinBox()
        player_count.setMinimum(1)
        # プレイ人数に応じて、プレイヤー名の設定数を変更する
        player_count.valueChanged.connect(lambda: self.createPlayerNameSetting(player_count, name_input_layout))
        layout.addRow("プレイ人数:", player_count)

        # プレイヤー名の設定
        player_name_setting = QLineEdit()
        name_input_layout.addRow(f"プレイヤー{layout.rowCount()}の名前:",player_name_setting)
        layout.addRow(name_input_layout)

        # ゲーム画面への遷移
        start_game_button = QPushButton("ゲーム開始")
        start_game_button.clicked.connect(lambda: self.startGame(name_input_layout))
        layout.addRow(start_game_button)
        
        self.w.setLayout(layout)

    def createPlayerNameSetting(self, player_count: QSpinBox, layout: QFormLayout):
        # プレイヤー名設定
        
        # 設定されたプレイヤー数
        count = player_count.value()
        # 表示されているプレイヤー名の入力欄数
        now_count = layout.rowCount()

        if now_count < count:
            for _ in range(count - now_count):
                player_name_setting = QLineEdit()
                layout.insertRow(layout.rowCount(), f"プレイヤー{layout.rowCount() + 1}の名前:", player_name_setting)
        elif now_count > count:
            for _ in range(now_count - count):
                layout.removeRow(layout.rowCount() - 1)
    
    def startGame(self, names_layout:QFormLayout):
        # プレイヤー名を格納する辞書型
        players_name = {}

        for j in range(names_layout.rowCount()):
            field = names_layout.itemAt(j, names_layout.ItemRole(1)).widget()
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

        # タスクリストの例
        # IPAの要件定義事例のシステム機能階層図の販売管理システム部分から引用
        self.ex_task_list = ["新規取引申請", "信用調査結果登録", "受注案件登録", "受注内容登録", "出荷予定登録", "出荷依頼"]

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
        # タスクを設定する画面部分全体のレイアウト
        task_set_layout = QFormLayout()
        # タスクを入力する入力フォームのペアのみを格納するレイアウト
        task_input_layout = QFormLayout()

        task_set_widget.setLayout(task_set_layout)

        task_set_layout.addRow(QLabel("タスクを設定..."))
        task_count = QSpinBox()
        task_count.setMinimum(1)
        task_count.valueChanged.connect(lambda: self.createTaskInputSetting(task_count, task_input_layout))
        task_set_layout.addRow("タスク数:", task_count)

        task_input_layout.addRow("タスク1つ目", QLineEdit())
        task_set_layout.addRow(task_input_layout)
        
        task_set_button = QPushButton("タスクを設定する")
        task_set_button.clicked.connect(lambda:game_preview.setCurrentIndex(1))
        task_set_button.clicked.connect(lambda:self.setTaskList(task_input_layout))
        task_set_layout.addRow(task_set_button)

        task_ex_layout = QVBoxLayout()
        task_ex = QPushButton("例")
        task_ex.clicked.connect(lambda:self.setExampleTask(task_input_layout, task_count))
        task_ex_layout.addWidget(task_ex,alignment=Qt.AlignmentFlag.AlignRight)
        task_set_layout.addRow(task_ex_layout)

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

        # プレイヤーの入力部の例
        input_ex = QPushButton("例")
        input_ex.clicked.connect(lambda:self.setExamplePlan(players_layout))
        self.w.layout().addWidget(input_ex, alignment=Qt.AlignmentFlag.AlignRight)

    def setTaskList(self, layout:QFormLayout):
        for i in range(layout.rowCount()):
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
            if rank_layout.count() > 4:
                rank_layout.addWidget(QLabel(f"6位以下の{len(sorted_rank_dict)-rank_layout.count()}個は省略"))
                break
        
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
                layout.addRow(f"タスク{layout.rowCount() + 1}つ目:", task_setting)
        elif now_count > count:
            for _ in range(now_count - count):
                layout.removeRow(layout.rowCount() - 1)

    def setExampleTask(self, layout: QFormLayout, spinbox: QSpinBox):
        # 入力フォームにタスク例の中から入れていく
        for i in range(layout.rowCount()):
            try:
                form:QLineEdit = layout.itemAt(i, layout.ItemRole(1)).widget()
                form.setText(self.ex_task_list[i])
            except :
                layout.removeRow(layout.rowCount() - 1)
                pass
        
        if layout.rowCount() != spinbox.value():
            spinbox.setValue(layout.rowCount())
    
    def setExamplePlan(self, layout: QGridLayout):
        return None
    
    def show(self):
        self.w.exec()