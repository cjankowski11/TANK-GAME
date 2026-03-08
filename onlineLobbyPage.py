from button import Button
import socket
import struct


class OnlineLobbyPage:

    def __init__(self, info):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100, (50, 50, 200), (80, 80, 250), 30)
        self.host = "127.0.0.1"
        self.port = 48874
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def draw_page(self, screen):
        self.back_button.draw(screen)

    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            self.info.online = None
            return "PLAY"
    
    def send_to_server_msg_that_i_exist(self):
        self.socket.sendto(struct.pack("B20s", 1, f"_NAME:{self.info.name}".encode()), (self.host, self.port))

