from button import Button
from text import Text
import socket
import struct
import threading
import time


class OnlineLobbyPage:

    def __init__(self, info):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100, (50, 50, 200), (80, 80, 250), 30)
        self.players_name_text = [Text("", 300, 200), Text("", 300, 245)
                                  , Text("", 300, 290), Text("", 300, 335)]
        self.names = []
        self.host = ""
        self.port = 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.settimeout(1)
        self.bot_text = Text("BOT", 525, 50)
        add_bot = Button("+", 500, 90, 100, 100, (50, 50, 200), (80, 80, 250))
        add_bot.change_to_sysfont("arial", 50)
        self.add_bot_button = add_bot
        sub_bot = Button("-", 625, 90, 100, 100, (50, 50, 200), (80, 80, 250))
        sub_bot.change_to_sysfont("arial", 50)
        self.subtract_bot_button = sub_bot

        # self.socket.bind((self.host, self.port))
        threading.Thread(target=self.recive, daemon=True).start()
        threading.Thread(target=self.send_to_server_msg_that_i_exist, daemon=True).start()

    def draw_page(self, screen):
        self.back_button.draw(screen)
        self.add_bot_button.draw(screen)
        self.subtract_bot_button.draw(screen)
        self.bot_text.draw(screen)
        for player_name in self.players_name_text:
            player_name.draw(screen)


    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            self.info.online = None
            return "PLAY"
        if self.add_bot_button.is_clicked(event):
            self.socket.sendto(struct.pack("B", 2), (self.host, self.port))
        if self.subtract_bot_button.is_clicked(event):
            self.socket.sendto(struct.pack("B", 3), (self.host, self.port))
    
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
                    names = msg.decode('utf-8').split(',')
                    self.names = [name.strip('\x00') for name in names]
                    for i in range(len(self.names)):
                        self.players_name_text[i].change_text(self.names[i])
                    for i in range(len(self.names), self.info.max_players):
                        self.players_name_text[i].change_text("")
                except socket.timeout:
                    continue
                except Exception as e:
                    print(e)

                time.sleep(1)