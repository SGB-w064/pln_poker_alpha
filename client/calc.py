import socket
import json
import pickle

import config

# サーバーのアドレス
adress = (config.address, 59630)

def calc_score(plan_list: dict, word: str):
    # 計算後の単語を格納する辞書型
    similarities_dict = {}

    cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cl.connect(adress)

    for plan in plan_list:
        send_data = pickle.dumps([plan, word])
        cl.send(send_data)

        similarities_dict[plan] = pickle.loads(cl.recv(1024))

    return json.dumps(similarities_dict, ensure_ascii=False)