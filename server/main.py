#!python3.8
import sys

# 自然言語処理のライブラリを立ち上げる
from module import calc

def main(args):
    # 起動時の引数に自然言語処理の種類を指定する
    # デフォルトはBERT
    if len(args) < 2:
        nlp_type = "BERT"
    else:
        nlp_type = args[1]
    
    server = calc.NLP_COS_SIMILARITY(nlp_type)
    server.startSimilarity()

    return None

if __name__ == "__main__":
    main(sys.argv)
