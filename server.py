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
                msg_type = struct.unpack("B", data[:1])[0]
                if msg_type == 1:
                    msg = struct.unpack("20s", data[1:])[0].decode()
                    print(msg)
                    self.players[addr] = (msg, time.time())
                    # print(self.players)

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
                self.delete_not_active()
                names = [value[0] for value in self.players.values()]
                msg = ",".join(names).encode('utf-8')
                for addr in list(self.players.keys()):
                    try:
                        self.socket.sendto(msg, addr)
                        self.socket.sendto(struct.pack("B80s", 1, msg), addr)
                    except Exception as e:
                        print(e)
            time.sleep(2)
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
            if time.time() - data[1] > 3:
                print(f"{data[0]} disconnected")
                addr_to_delete.append(addr)
        for addr in addr_to_delete:
            self.players.pop(addr)


server = Server("", )
server.run()