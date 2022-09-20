#!python3.8

# socket通信関係
import socket
import threading

###
### お題に沿った文を参加者が出し合い、タスクごとの関連性をランキング付けする
###

class PLN_POKER_SERVER:
    def __init__(self):
        self.players = []
