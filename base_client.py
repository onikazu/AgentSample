from socket import *
import threading
import sys
import os


class BasePlayer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)

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
            print(message)
            self.analyzeMessage(message)


    # messageの解析を行う関数
    def analyzeMessage(self, message):
        return


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = BasePlayer()
        players.append(p)
        if i < 11:
            team_name = "Left"
        else:
            team_name = "Right"
        players[i].initialize(i%11+1, team_name, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
