"""
基本的な機能を備えたサッカーエージェント
戦略等は未実装
"""

from socket import *
import threading
import sys
import os
import csv

from analyze import *


class BaseClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # サーバ接続のための変数
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)

        # クライアントの基本情報を代入する変数
        self.m_iNumber = 0
        self.m_strTeamName = ""
        self.m_strHostName = ""
        self.m_kick_off_x = 0
        self.m_kick_off_y = 0


        # メッセージの解析結果を代入する変数
        self.init_result = {}
        self.visual_result = {}
        self.physical_result = {}
        self.aural_result = {}
        self.player_type_result = {}
        self.player_param_result = {}
        self.server_param_result = {}

        # コマンドを代入する変数
        self.m_strCommand = ""

        # フィールドのモードを代入する変数
        self.play_mode = ""

    # コマンドの送信
    def send(self, command):
        if len(command) == 0:
            return
        command = command + "\0"
        try:
            to_byte_command = command.encode(encoding='utf_8')
            self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))
        except OSError:
            print("送信失敗")
            sys.exit()

    # メッセージの受信を行う関数
    def receive(self):
        try:
            message, arr = self.socket.recvfrom(4096)
            message = message.decode("UTF-8")
            self.PORT = arr[1]
            if self.m_iNumber == 1:
                print(message)
            return message
        except OSError:
            print("受信失敗")
            sys.exit()

    # クライアントの登録を行う関数
    def initialize(self, number, team_name, server_name, server_port):
        self.m_iNumber = number
        self.m_strTeamName = team_name
        self.m_strHostName = server_name
        self.PORT = server_port
        if self.m_iNumber == 1:
            command = "(init " + self.m_strTeamName + "(goalie)(version 15.40))"
        else:
            command = "(init " + self.m_strTeamName + "(version 15.40))"
        self.send(command)

    # thread を動かしている最中に行われる関数
    def run(self):
        while True:
            message = self.receive()
            # print(message)
            self.analyzeMessage(message)

    # messageの解析を行う関数
    def analyzeMessage(self, message):
        if message.startswith("(init "):
            self.init_result = analyze.analyzeInitialMessage(message)
            self.play_mode = self.init_result["play_mode"]
        # 視覚メッセージの処理
        elif message.startswith("(see "):
            self.visual_result = analyze.analyzeVisualMessage(message, \
            self.play_mode, self.m_kick_off_x, self.m_kick_off_y)
        # 体調メッセージの処理
        elif message.startswith("(sense_body "):
            self.physical_result = analyze.analyzePhysicalMessage(message)
            self.play(self.init_result, self.visual_result, self.aural_result, \
            self.physical_result, self.player_type_result)
        # 聴覚メッセージの処理
        elif message.startswith("(hear "):
            self.aural_result, play_mode = analyze.analyzeAuralMessage(message)
            # プレイモードが観測できたら更新
            if play_mode == "":
                self.play_mode = play_mode
        # サーバパラメータの処理
        elif message.startswith("(server_param"):
            self.server_param_result = analyze.analyzeServerParam(message)
        # プレーヤーパラメータの処理
        elif message.startswith("(player_param"):
            self.player_param_result = analyze.analyzePlayerParam(message)
        # プレーヤータイプの処理
        elif message.startswith("(player_type"):
            self.player_type_result = analyze.analyzePlayerType(message)
        # エラーの処理
        else:
            print("サーバーからエラーが伝えられた:", message)
            print("エラー発生原因のコマンドは右記の通り :", self.m_strCommand)

    def play(self, init_result, visual_result, aural_result, physical_result, player_type_result):
        if analyze.checkInitialMode(self.play_mode):
            self.setKickOffPosition()
            command = "(move " + str(self.m_kick_off_x) + " " \
                + str(self.m_kick_off_y) + ")"
            self.send(command)

    def setKickOffPosition(self):
        with open("./formation/init.csv", "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if self.m_iNumber == row[0]:
                    self.m_kick_off_x = row[1]
                    self.m_kick_off_y = row[2]


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = BaseClient()
        players.append(p)
        if i < 11:
            team_name = "Left"
        else:
            team_name = "Right"
        players[i].initialize(i%11+1, team_name, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
