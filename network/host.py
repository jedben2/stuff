import socket
# import threading
from netifaces import interfaces, ifaddresses, AF_INET
import time
from host_mods.player import *


class Host:
    @staticmethod
    def _get_ip():
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': ''}])]
            for a in addresses:
                if a != '' and a != "127.0.0.1":
                    return a

    def __init__(self, port, localhost):
        self.port = port
        self.ip = self._get_ip()
        if localhost: self.ip = '127.0.0.1'
        self.conns = []

    def handle_data(self, data):
        datas = data.split('/')

    # def manage_conn(self, conn, addr):
    #     print(f"Connected {addr}")
    #     connected = True
    #     while connected:
    #         time.sleep(2)
    #         conn.send(b't')
    #         data = conn.recv(1024).decode()
    #         print(data)
    #         if data == "exit": connected = False
    #         elif data == "connected?": conn.send(b'yes')
    #     print("closed")
    #     conn.close()
    #     self.conns.remove(conn)
    #     return

    def start(self):
        players = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            for i in range(1):
                s.listen()
                conn, addr = s.accept()
                players.append(Player(position=(-5 + 10 * i, 0), conn=conn, addr=addr))
                print(addr)

            playing = True
            while playing:
                for player in players:
                    player.conn.send(" ".encode())
                    player.on_floor, player.held_keys = player.conn.recv(1024).decode().split('/')
                    player.held_keys = dict(player.held_keys)
                    player.move()
                for player in players:
                    player.conn.send(f"{player.x}/{player.y}/{player.frame}/{player.direction}".encode())
                time.sleep(1/60)

if __name__ == '__main__':
    host = Host(2000, True)
    host.start()
