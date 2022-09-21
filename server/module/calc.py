#!python3.8

# socket通信関連
import socket
import threading
import pickle

# fastText関連
import numpy
from gensim.models import fasttext

###
### 自然言語処理を使用し、渡された2つの単語の類似度を返すサーバー
###

class NLP_COS_SIMILARITY():
    def __init__(self, nlp_type="BERT"):
        self.nlp_type = nlp_type    # 自然言語処理の種類
    
    # 接続したクライアントとのやり取り
    def connetClient(self, cl, cla, calc_func):
        while True:
            data = pickle.loads(cl.recv(1024))
            
            # 送られてくるデータは比較する2つの単語のリストと仮定
            # 例 data = ["hoge", "huga"]
            if type(data) is list and len(data) == 2:
                cl.send(pickle.dumps(calc_func(data[0], data[1])))
            elif data == "end":
                # 特に理由はないがサーバーを閉じる文字列を含める
                self.server.close()
            else:
                # 上記以外のデータが来た場合の返信
                cl.send("計算失敗".encode("utf-8"))

    # サーバーの立ち上げ    
    def startServer(self, calc_func):
        self.address = (socket.gethostbyname(socket.gethostname()), 59630)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.server.listen(1)
        print("starting server")

        while True:
            cl, cla = self.server.accept()
            print(cl, cla)
            thread = threading.Thread(target=self.connetClient, args=(cl, cla, calc_func))
            thread.start()

        self.server.close()

    # fastText用の計算部分
    def calcScoreForFastText(self, plan: str, word: str):
        
        return self.model.wv.similarity(plan, word).astype(numpy.unicode)

    # fastTextの立ち上げ
    def fastTextCalc(self):
        self.model_path = "./models/wiki.ja/wiki.ja.bin"
        self.model = fasttext.load_facebook_model(self.model_path)

        self.startServer(self.calcScoreForFastText)

    # 処理全体の開始
    def startSimilarity(self):
        if self.nlp_type == "fastText":
            self.fastTextCalc()
