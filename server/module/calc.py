#!python3.8

# socket通信関連
import socket
import threading

# fastText関連
import numpy
from gensim.models import fasttext

###
### 自然言語処理を使用し、渡された2つの単語の類似度を返すサーバー
###

class NLP_COS_SIMILARITY():
    def __init__(self, nlp_type="BERT"):
        self.nlp_type = nlp_type
    
    def connetClient(self, cl, cla, calc_func):
        while True:
            data = cl.recv(1024).decode("utf-8")
            
            if " " in data:
                plan, idea = tuple(data.split(" "))
                cl.send(calc_func(plan, idea).encode("utf-8"))
            elif data == "end":
                self.server.close()
            else:
                cl.send("計算失敗".encode("utf-8"))
        

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

    def calcScoreForFastText(self, plan: str, word: str):
        
        return self.model.wv.similarity(plan, word).astype(numpy.unicode)

    def fastTextCalc(self):
        self.model_path = "./models/wiki.ja/wiki.ja.bin"
        self.model = fasttext.load_facebook_model(self.model_path)

        self.startServer(self.calcScoreForFastText)

    def startSimilarity(self):
        if self.nlp_type == "fastText":
            self.fastTextCalc()
