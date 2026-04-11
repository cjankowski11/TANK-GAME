from button import Button
from text import Text
import socket
import struct
import threading
import time


class OnlineLobbyPage:

    def __init__(self, info, host="127.0.0.1", port=12345):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100, (50, 50, 200), (80, 80, 250), 30)
        self.players_name_text = [Text("", 300, 150), Text("", 300, 195)
                                  , Text("", 300, 240), Text("", 300, 295)]
        for text in self.players_name_text:
            text.change_to_sysfont("arial", 30)
        
        self.names = []
        self.is_ready = []
        self.host = host
        self.port = port
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

        self.rounds_text = Text(f"ROUNDS {self.info.number_of_rounds}", 250, 50)
        add_round = Button("+", 250, 90, 100, 100, (50, 50, 200), (80, 80, 250))
        add_round.change_to_sysfont("arial", 50)
        self.add_round_button = add_round
        sub_round = Button("-", 375, 90, 100, 100, (50, 50, 200), (80, 80, 250))
        sub_round.change_to_sysfont("arial", 50)
        self.subtract_round_button = sub_round

        self.ready_button = Button("READY", 50, 340, 300, 100, (50, 50, 200), (80, 80, 250), 50)
        self.start_button = Button("START", 450, 340, 300, 100, (50, 50, 200), (80, 80, 250), 50)

        # self.socket.bind((self.host, self.port))
        # threading.Thread(target=self.recive, daemon=True).start()
        # threading.Thread(target=self.send_to_server_msg_that_i_exist, daemon=True).start()
        self.ready = False

    def start_connection(self):         # should i end threads when i exit from onlinePage?hmm
        threading.Thread(target=self.recive, daemon=True).start()
        threading.Thread(target=self.send_to_server_msg_that_i_exist, daemon=True).start()

    def draw_page(self, screen):
        self.back_button.draw(screen)
        self.add_bot_button.draw(screen)
        self.subtract_bot_button.draw(screen)
        self.bot_text.draw(screen)
        self.ready_button.draw(screen)
        self.start_button.draw(screen)
        self.rounds_text.draw(screen)
        self.add_round_button.draw(screen)
        self.subtract_round_button.draw(screen)
        for player_name in self.players_name_text:
            player_name.draw(screen)


    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            self.info.online = None
            self.ready = False
            return "PLAY"
        if self.add_bot_button.is_clicked(event):
            self.socket.sendto(struct.pack("B", 2), (self.host, self.port))
        if self.subtract_bot_button.is_clicked(event):
            self.socket.sendto(struct.pack("B", 3), (self.host, self.port))
        if self.ready_button.is_clicked(event):
            self.ready = not self.ready
        if self.start_button.is_clicked(event):
            self.socket.sendto(struct.pack("B", 4), (self.host, self.port))
        if self.add_round_button.is_clicked(event):   #zmienic to na serwer
            self.socket.sendto(struct.pack("B", 5), (self.host, self.port))
        if self.subtract_round_button.is_clicked(event):
            self.socket.sendto(struct.pack("B", 6), (self.host, self.port))

        
        
    
    def send_to_server_msg_that_i_exist(self):
        while self.info.online and not self.info.game_running:
            try:
                self.socket.sendto(struct.pack("B?20s", 1, self.ready, self.info.name.encode()), (self.host, self.port))
            except Exception as e:
                print(e)
            time.sleep(0.5)

    def recive(self):
        while self.info.online and not self.info.game_running:
            try:
                msg, _ = self.socket.recvfrom(2048)
                msg_type = int(msg[0])

                if msg_type == 0:
                    num_players, num_bots, rounds = struct.unpack("BBB", msg[1:4])
                    msg = msg[4:]
                    self.info.number_of_bots = num_bots
                    self.info.number_of_rounds = rounds
                    self.names = []
                    self.is_ready = []
                    for _ in range(num_players):
                        is_ready, name = struct.unpack("?20s", msg[:21])
                        name = name.decode().rstrip("\x00")
                        self.names.append(name)
                        self.is_ready.append(is_ready)
                        msg = msg[21:]
                    self.update_players()
                    self.update_rounds()

                if msg_type == 1:
                    self.info.socket = self.socket
                    self.info.game_running = True
                    break
                
                if msg_type == 2:  # make it better looking
                    break

                
            except socket.timeout:
                continue
            except Exception as e:
                print(e)
            time.sleep(0.01)
    
    def update_players(self):
        for i in range(len(self.names)):
            self.players_name_text[i].change_text(self.names[i])
            if self.is_ready[i]:
                self.players_name_text[i].change_color((0, 255, 0))
            else:
                self.players_name_text[i].change_color((255, 0, 0))
        for i in range(len(self.names), len(self.names)+self.info.number_of_bots):
            self.players_name_text[i].change_text("BOT")
            self.players_name_text[i].change_color((255, 255, 255))
        
        for i in range(len(self.names)+self.info.number_of_bots, self.info.max_players):
            self.players_name_text[i].change_text("")
    
    def update_rounds(self):
        self.rounds_text.change_text(f"ROUNDS {self.info.number_of_rounds}")