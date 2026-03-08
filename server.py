import socket
import threading
import time
import struct


class Server:
    def __init__(self, host='127.0.0.1', port=34567):
        self.host = host
        self.port = port

        self.kill = False
        self.thread_count = 0
        self.players = {}
        self.max_players = 4
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(1)

    def handle_data(self, data, addr):
        try:
            if len(data):
                # data = struct.unpack_from("ff", data, 0)
                print(data)
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


    def listen_loop(self):
        self.thread_count += 1
        print("Server working")
        while not self.kill:
            try:
                data, addr = self.socket.recvfrom(2048)
                self.handle_data(data, addr)
            except socket.timeout:
                continue
            time.sleep(0.01)
        self.thread_count -= 1

    def broadcasting(self):
        self.thread_count += 1
        while not self.kill:
            if self.players:
                for addr in list(self.players.keys()):
                    for _, name in self.players.items():
                        packet = struct.pack("B20s", 1, name.encode())
                        try:
                            self.socket.sendto(packet, addr)
                        except Exception as e:
                            print(e)
            time.sleep(1)
        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("killed")

    def run(self):
        threading.Thread(target=self.listen_loop).start()
        # threading.Thread(target=self.broadcasting).start()
        try:
            while True:
                time.sleep(0.05)
                # print("ez")
        except KeyboardInterrupt:
            self.await_kill()


server = Server("127.0.0.1", )
server.run()