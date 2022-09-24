#!python3.8

# socket通信関連
import socket
import threading
import json

# fastText関連
import numpy
from gensim.models import fasttext

# BERT関連
from transformers import BertJapaneseTokenizer, BertModel
import torch

###
### 自然言語処理を使用し、渡された2つの単語の類似度を返すサーバー
###

class NLP_COS_SIMILARITY():
    def __init__(self, nlp_type="BERT"):
        self.nlp_type = nlp_type    # 自然言語処理の種類
    
    # 接続したクライアントとのやり取り
    def connetClient(self, cl, cla, calc_func):
        while True:
            # json型のオブジェクトを文字列化されたものだけ受け取る
            try:
                data = json.loads(cl.recv(1024).decode("utf-8"))
            except:
                # 上記以外の文字列が来た場合
                cl.send("計算失敗".encode("utf-8"))
            
            # 送られてくるデータは比較する2つの単語の辞書と仮定
            # 例 data = ["hoge", "huga"]
            if type(data) is dict and list(data.keys()) == ["word1", "word2"]:
                cl.send(calc_func(data["word1"], data["word2"]).encode("utf-8"))
            else:
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
    def calcFastText(self):
        self.model_path = "./models/wiki.ja/wiki.ja.bin"
        self.model = fasttext.load_facebook_model(self.model_path)

        self.startServer(self.calcScoreForFastText)
    
    # BERTでの特徴量抽出関数
    def calcEmbeddingForBert(self, text: str):
        ids = torch.tensor(self.tokenizer.encode(text, add_special_tokens=True)).unsqueeze(0)

        output = self.model_bert(ids)
        return output.last_hidden_state[0][0]

    # BERTでのcos類似度計算部分
    def calcCosSimForTorch(self, a, b):
        return torch.dot(a, b) / (torch.linalg.norm(a) * torch.linalg.norm(b))

    # BERT用の計算部分
    def calcScoreForBert(self, plan: str, word: str):
        # Tensor型の指数表記を解除する
        torch.set_printoptions(sci_mode=False)
        return str(self.calcCosSimForTorch(self.calcEmbeddingForBert(plan), self.calcEmbeddingForBert(word)).item())

    # BERTの立ち上げ
    def calcBert(self):
        self.model_path = "cl-tohoku/bert-base-japanese-whole-word-masking"
        self.tokenizer = BertJapaneseTokenizer.from_pretrained(self.model_path)
        self.model_bert = BertModel.from_pretrained(self.model_path)

        self.startServer(self.calcScoreForBert)

    # 処理全体の開始
    def startSimilarity(self):
        if self.nlp_type == "fastText":
            self.calcFastText()
        elif self.nlp_type == "BERT":
            self.calcBert()
