import socket
import json

import config

# サーバーのアドレス
adress = (config.calc_address, config.calc_port)

def calc_score_for_test(plan_list: dict, word: str):
    # 計算後の単語を格納する辞書型
    similarities_dict = {}

    cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cl.connect(adress)

    for plan in plan_list:
        send_data = json.dumps({"word1" : plan, "word2" : word})
        cl.send(send_data.encode("utf-8"))

        similarities_dict[plan] = cl.recv(1024).decode("utf-8")

    return json.dumps(similarities_dict, ensure_ascii=False)

def calc_score(plan: str, word: str):

    cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cl.connect(adress)

    send_data = json.dumps({"word1" : plan, "word2" : word})
    cl.send(send_data.encode("utf-8"))

    ans = cl.recv(1024).decode("utf-8")

    cl.close()

    return ans

def main():
    word1 = input("word1 : ")
    word2 = input("word2 : ")
    ans = calc_score(word1, word2)
    print(ans)

if __name__ == "__main__":
    main()
