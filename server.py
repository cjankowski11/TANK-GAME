import socket
import threading
import time
import struct


class Server:
    def __init__(self, host='127.0.0.1', port=48874):
        self.host = host
        self.port = port

        self.kill = False
        self.thread_count = 0
        self.players = {}
        self.max_players = 4

    def handle_data(self, data, addr, socket):
        # self.thread_count += 1
        try:
            if len(data):
                # data = struct.unpack_from("ff", data, 0)
                msg_type = struct.unpack("B", data[:1])[0]
                if msg_type == 1:
                    msg = struct.unpack("20s", data[1:])[0]
                    print(msg)
                # decoded_data = data.decode()
                # print(decoded_data)
                # for player in self.players:
                #     socket.sendto(data, player)
        except Exception as e:
            print(f"error {e}")
        # self.thread_count -= 1


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
                    # if addr not in self.players:
                    #     self.players.append(addr)
                    self.handle_data(data, addr, s)
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


server = Server("127.0.0.1", 48874)
server.run()