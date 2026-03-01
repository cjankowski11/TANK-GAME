import socket
import threading
import time
import struct


class Server:
    def __init__(self, host='127.0.0.1', port=63659):
        self.host = host
        self.port = port

        self.kill = False
        self.thread_count = 0
        self.players = []

    def connection_listen_loop(self):
        self.thread_count += 1
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)  # not necesarilly needed
            s.bind((self.host, self.port))

            while not self.kill:
                s.settimeout(1)
                try:
                    data, addr = s.recvfrom(2048)
                    print(data, addr)
                    if addr not in self.players:
                        self.players.append(addr)
                except socket.timeout:
                    continue
                time.sleep(0.01)
        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("killed")

    def run(self):
        threading.Thread(target=self.connection_listen_loop).start()
        try:
            while True:
                time.sleep(0.05)
                # print("ez")
        except KeyboardInterrupt:
            self.await_kill()


server = Server()
server.run()