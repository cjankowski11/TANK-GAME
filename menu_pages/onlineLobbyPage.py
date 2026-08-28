from menu_utilities.button import Button
from menu_utilities.text import Text
import socket
import struct
import threading
import time
import network_constants as nc


class OnlineLobbyPage:

    def __init__(self, info, socket, host="127.0.0.1", port=12345):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100)
        self.players_name_text = [Text("", 300, 150), Text("", 300, 195),
                                  Text("", 300, 240), Text("", 300, 295)]
        for text in self.players_name_text:
            text.change_to_sysfont("arial")
        
        self.players = {}
        self.host = host
        self.port = port
        self.socket = socket
        self.bot_text = Text("BOT", 525, 50)
        add_bot = Button("+", 500, 90, 100, 100)
        add_bot.change_to_sysfont("arial", 50)
        self.add_bot_button = add_bot
        sub_bot = Button("-", 625, 90, 100, 100)
        sub_bot.change_to_sysfont("arial", 50)
        self.subtract_bot_button = sub_bot

        self.rounds_text = Text(f"ROUNDS {self.info.number_of_rounds}", 250, 50)
        add_round = Button("+", 250, 90, 100, 100)
        add_round.change_to_sysfont("arial", 50)
        self.add_round_button = add_round
        sub_round = Button("-", 375, 90, 100, 100)
        sub_round.change_to_sysfont("arial", 50)
        self.subtract_round_button = sub_round

        self.ready_button = Button("READY", 50, 340, 300, 100, font_size=50)
        self.start_button = Button("START", 450, 340, 300, 100, font_size=50)

        self.ready = False

    def start_connection(self):
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
            self.socket.sendto(
                struct.pack("B", nc.ADD_BOT), (self.host, self.port))
        if self.subtract_bot_button.is_clicked(event):
            self.socket.sendto(
                struct.pack("B", nc.REMOVE_BOT), (self.host, self.port))
        if self.ready_button.is_clicked(event):
            self.ready = not self.ready
        if self.start_button.is_clicked(event):
            self.socket.sendto(
                struct.pack("B", nc.START_GAME), (self.host, self.port))
        if self.add_round_button.is_clicked(event):
            self.socket.sendto(
                struct.pack("B", nc.ADD_ROUND), (self.host, self.port))
        if self.subtract_round_button.is_clicked(event):
            self.socket.sendto(
                struct.pack("B", nc.REMOVE_ROUND), (self.host, self.port))

    def send_to_server_msg_that_i_exist(self):
        while self.info.online:
            name = self.info.name.encode()
            name_length = len(name)
            try:
                self.socket.sendto(
                    struct.pack(f"BB?{name_length}s",
                                nc.PLAYER_NAME_AND_READY_STATUS,
                                name_length, self.ready, name), (self.host, self.port))
            except Exception as e:
                print(e)
            time.sleep(0.5)

    def recive(self):
        while self.info.online and not self.info.game_running:
            try:
                msg, _ = self.socket.recvfrom(2048)
                msg_type = int(msg[0])
                print(f"LOBBY: {msg_type}")
                if msg_type == nc.ACTIVE_PLAYERS:
                    num_players, num_bots, rounds = struct.unpack("BBB", msg[1:4])
                    msg = msg[4:]
                    self.info.number_of_bots = num_bots
                    self.info.number_of_rounds = rounds
                    self._update_players(num_players, msg)
                    self._display_updated_players()
                    self.update_rounds()
                    
                if msg_type == nc.START_GAME:
                    print("START")
                    self.info.socket = self.socket
                    self.info.game_running = True
                    break

            except socket.timeout:
                continue
            except Exception as e:
                print(e)
            time.sleep(0.01)
    
    def _display_updated_players(self):
        place = 0
        for name, is_ready in self.players.items():
            self.players_name_text[place].change_text(name)
            if is_ready:
                self.players_name_text[place].change_color((0, 255, 0))
            else:
                self.players_name_text[place].change_color((255, 0, 0))
            place += 1

        for _ in range(self.info.number_of_bots):
            self.players_name_text[place].change_text("BOT")
            self.players_name_text[place].change_color((255, 255, 255))
            place += 1
        
        for _ in range(place, self.info.max_players):
            self.players_name_text[place].change_text("")
            place += 1

    def update_rounds(self):
        self.rounds_text.change_text(f"ROUNDS {self.info.number_of_rounds}")

    def _update_players(self, num_players, msg):
        self.players = {}
        for _ in range(num_players):
            name_length, is_ready = struct.unpack("B?", msg[:2])
            encoded_name = struct.unpack(f"{name_length}s", msg[2:name_length+2])[0]
            name = encoded_name.decode()
            self.players[name] = is_ready
            msg = msg[name_length+2:]
