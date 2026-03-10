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
        self.bots_number = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(1)
        self.lock = threading.Lock()

    def handle_data(self, data, addr):
        try:
            if len(data):
                msg_type = struct.unpack("B", data[:1])[0]
                if addr in self.players:
                    self.players[addr]["time"] = time.time()
                with self.lock:
                    if msg_type == 1:
                        ready, name = struct.unpack("?20s", data[1:])
                        all_players = self.get_players_number() + self.bots_number
                        if all_players < 4 or addr in self.players:
                            self.players[addr] = {"name": name.decode(),
                                                  "time": time.time(),
                                                  "ready": ready}

                        # print(self.players)
                    if msg_type == 2:
                        # print("add bot")
                        if self.bots_number + self.get_players_number() < 4:
                            self.bots_number += 1
                    
                    if msg_type == 3:
                        # print("sub bot")
                        if self.bots_number > 0:
                            self.bots_number -= 1

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
            except Exception as e:
                print(e)
            time.sleep(0.01)
        self.thread_count -= 1

    def broadcasting(self):  
        self.thread_count += 1
        while not self.kill:
            if self.players:
                with self.lock:
                    self.delete_not_active()
                    buffor = struct.pack("BB", len(self.players), self.bots_number)
                    for value in self.players.values():
                        buffor += struct.pack("?20s", value["ready"], (value["name"]).encode())

                for addr in list(self.players.keys()):
                    try:
                        self.socket.sendto(buffor, addr)
                    except Exception as e:
                        print(e)
            time.sleep(0.1)
        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("killed")

    def run(self):
        threading.Thread(target=self.listen_loop).start()
        threading.Thread(target=self.broadcasting).start()
        try:
            while True:
                time.sleep(0.05)
                # print("ez")
        except KeyboardInterrupt:
            self.await_kill()

    
    def delete_not_active(self):
        addr_to_delete = []
        for addr, data in self.players.items():
            if time.time() - self.players[addr]["time"] > 5:
                print(f"{self.players[addr]["name"]} disconnected")
                addr_to_delete.append(addr)
        for addr in addr_to_delete:
            self.players.pop(addr)

    def get_players_number(self):
        return len(self.players.keys())

server = Server("")
server.run()