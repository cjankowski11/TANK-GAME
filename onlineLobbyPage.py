from button import Button
import socket
import struct
import threading
import time


class OnlineLobbyPage:

    def __init__(self, info):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100, (50, 50, 200), (80, 80, 250), 30)
        self.host = ""
        self.port = 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.settimeout(1)
        # self.socket.bind((self.host, self.port))
        threading.Thread(target=self.recive, daemon=True).start()
        threading.Thread(target=self.send_to_server_msg_that_i_exist, daemon=True).start()

    def draw_page(self, screen):
        self.back_button.draw(screen)


    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            self.info.online = None
            return "PLAY"
    
    def send_to_server_msg_that_i_exist(self):
        while True:
            while self.info.online:
                try:
                    self.socket.sendto(struct.pack("B20s", 1, self.info.name.encode()), (self.host, self.port))
                except Exception as e:
                    print(e)
                time.sleep(1)

    def recive(self):
        while True:
            while self.info.online:
                try:
                    msg, _ = self.socket.recvfrom(2048)
                    msg.decode()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(e)

                time.sleep(1)