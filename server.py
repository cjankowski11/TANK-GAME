import socket
import threading
import time
import struct
from gameEngine import GameEngine
from dotenv import load_dotenv
import os
from player import Player, BotPlayer
import network_constants as nc
load_dotenv()
server_ip = os.getenv("SERVER_IP")
port = os.getenv("PORT")

MAX_ROUNDS = 20


class Server:
    def __init__(self, host='127.0.0.1', port=34567):
        self.host = host
        self.port = port
        self.start_game = False
        self.kill = False
        self.thread_count = 0
        self.players = {}
        self.max_players = 4
        self.bots_number = 0
        self.rounds_number = 1
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(1)
        self.lock = threading.Lock()

    def handle_data(self, data, addr):
        if len(data):
            msg_type = struct.unpack("B", data[:1])[0]
            if msg_type <= 7:
                self.handle_lobby_data(msg_type, data[1:], addr)
            else:
                self.handle_game_data(msg_type, data[1:], addr)

    def handle_lobby_data(self, msg_type, data, addr):
        if msg_type == nc.VALIDATE_PLAYER_NAME:
            self.validate_player_name(data, addr)
        elif msg_type == nc.PLAYER_NAME_AND_READY_STATUS:
            self.update_player_activity(data, addr)
        elif msg_type == nc.ADD_BOT:
            self.add_bot()
        elif msg_type == nc.REMOVE_BOT:
            self.remove_bot()
        elif msg_type == nc.START_GAME:
            self.check_ready_status_and_set_start()
        elif msg_type == nc.ADD_ROUND:
            self.add_round()
        elif msg_type == nc.REMOVE_ROUND:
            self.remove_round()

    def check_ready_status_and_set_start(self):
        with self.lock:
            if (not self.start_game and
               self.bots_number + self.get_players_number() > 1):
                self.start_game = (bool(self.players) and all(player.ready
                                   for player in self.players.values()))
                self.initialize_bots()

    def remove_round(self):
        with self.lock:
            if self.rounds_number > 1:
                self.rounds_number -= 1

    def add_round(self):
        with self.lock:
            if self.rounds_number < MAX_ROUNDS:
                self.rounds_number += 1

    def remove_bot(self):
        with self.lock:
            if self.bots_number > 0:
                self.bots_number -= 1

    def add_bot(self):
        with self.lock:
            if self.bots_number + self.get_menu_players_number() < 4:
                self.bots_number += 1

    def update_player_activity(self, data, addr):
        now = time.time()
        name_length, ready_status = struct.unpack("B?", data[:2])
        name_raw = struct.unpack(f"{name_length}s", data[2:name_length+2])[0]
        decoded_name = name_raw.decode()
        with self.lock:
            all_players = self.get_players_number() + self.bots_number
            addrs = self.get_players_addrs()
            if all_players < 4 and addr not in addrs:
                self.players.append(Player(decoded_name, ready_status, now))
            if addr in addrs:
                player = self.players[addr]
                player.set_ready(ready_status)
                player.set_last_active_time(now)
                player.set_name(decoded_name)

    def validate_player_name(self, data, addr):
        name_is_used = False
        name_length = struct.unpack("B", data[:1])[0]
        new_name = struct.unpack(f"{name_length}s", data[1:int(name_length)+2])[0]
        new_name = new_name.decode()
        with self.lock:
            name_is_used = any(
                player.name == new_name for player in self.players
                )
        self.socket.sendto(
            struct.pack("B?", nc.NAME_VALIDATION_RESPONSE, name_is_used), addr)
        
    def handle_game_data(self, msg_type, data, addr):
        if msg_type == nc.PLAYER_INSTRUCTIONS:
            self.update_player_instructions(data, addr)

    def update_player_instructions(self, data, addr):
        w, a, s, d, shoot = struct.unpack("BBBBB", data)
        with self.lock:
            self.players[addr].update(w, a, s, d, shoot)

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
            # time.sleep(0.01)
        self.thread_count -= 1

    def broadcasting(self):
        game_initialized = False
        ticks_per_sec = 60
        tick_duration = 1.0 / ticks_per_sec
        current_round = 0
        self.thread_count += 1
        next_tick = time.time()
        start_msg_send = False
        while not self.kill:
            now = time.time()
            
            with self.lock:
                active_game = self.start_game
                current_players_addr = list(self.players.keys())

            if not active_game:
                self.resending_active_players()
                time.sleep(0.1)

                next_tick = time.time()
                current_round = 0
                continue

            if not start_msg_send:
                for addr in current_players_addr:
                    self.socket.sendto(struct.pack("B", nc.START_GAME), addr)
                    start_msg_send = True

            if not game_initialized:
                self.initialize_game(ticks_per_sec)
                self.update_bot_walls()
                current_round += 1
                if current_round > self.rounds_number:
                    self.start_game = False
                    continue

                game_initialized = True
                
                time.sleep(0.1)
                for _ in range(5):
                    self.send_starting_info()
                    time.sleep(0.5)

                next_tick = time.time() + tick_duration 
            # dodac resetowanie zamiast tworzenia nowego obiektu(gmaeengine)
            if now >= next_tick:
                if self.gameEngine.is_finished():
                    game_initialized = False
                    self.add_point_for_the_winner()
                    if current_round == self.rounds_number:
                        for addr in current_players_addr:
                            self.socket.sendto(struct.pack("B", nc.END_GAME), addr)
                        with self.lock:
                            self.players = {}
                        start_msg_send = False
                        
                self.update_game_logic()  
                self.broadcast_game_state() 
                next_tick += tick_duration
            else:
                time.sleep(0.001)
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
            while not self.kill:
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            self.await_kill()

    def add_point_for_the_winner(self):
        winner = self.gameEngine.get_winner()
        winner.add_point()
        for player in self.players.values():
            print(f"player {player.name} has {player.points} points")

    def delete_not_active(self):
        addr_to_delete = []
        for addr, _ in self.players.items():
            if time.time() - self.players[addr].last_active_time > 5:
                addr_to_delete.append(addr)
        for addr in addr_to_delete:
            self.players.pop(addr)

    def get_players_number(self):
        return len(self.players)
    
    def get_players_addrs(self):
        return list(self.players.keys())

    def get_players(self):
        return list(self.players.values())
    
    def get_player_name(self, addr):
        return self.menu_players[addr].name
    
    def resending_active_players(self):
        with self.lock:
            self.delete_not_active()
            current_players = self.get_players()
            num_players = self.get_players_number()
            current_bots = self.bots_number
            rounds = self.rounds_number
        buffor = struct.pack("BBBB", nc.ACTIVE_PLAYERS, num_players, current_bots, rounds)
        for player in current_players:
            encoded_name = player.name.encode()
            name_length = len(encoded_name)
            buffor += struct.pack(f"B?{name_length}s", name_length, player.ready, encoded_name)
        with self.lock:
            addrs = self.get_players_addrs()

        for addr in addrs:
            try:
                self.socket.sendto(buffor, addr)
            except Exception as e:
                print(e)
            
    def initialize_game(self, tps):
        with self.lock:
            players = self.get_players()
            for player in players:
                player.alive = True

        self.gameEngine = GameEngine(players, tps)
                
    def initialize_bots(self):
        for i in range(self.bots_number):
            bot_name = f"BOT{i}"
            self.players[bot_name] = BotPlayer(bot_name)

    def update_game_logic(self):
        bullets_info = self.gameEngine.get_bullets()
        players_info = self.gameEngine.get_players()
        with self.lock:
            players = self.get_players()
        for player in players:
            if player.is_bot():
                player.update_bullets(bullets_info)
                player.update_players(players_info)
                player.update()
        with self.lock:
            for player in players:
                instructions = player.get_instructions()
                name = player.name
                self.gameEngine.update_tank(
                    name, instructions["w"], instructions["a"],
                    instructions["s"], instructions["d"],
                    instructions["shoot"])
        self.gameEngine.update_bullets()
            
    def broadcast_game_state(self):
        players = self.gameEngine.get_players(binary=True)
        bullets = self.gameEngine.get_bullets(binary=True)
        msg = struct.pack("B", nc.PLAYERS_AND_BULLETS) + players + bullets

        with self.lock:
            addrs = self.get_players_addrs()
        for addr in addrs:
            self.socket.sendto(msg, addr)

    def send_starting_info(self):
        walls = self.gameEngine.get_walls(binary=True)
        players = self.gameEngine.get_players(binary=True)
        msg = struct.pack("B", nc.STARTING_WALLS_AND_PLAYERS) + walls + players
        with self.lock:
            addrs = self.get_players_addrs()
        for addr in addrs:
            self.socket.sendto(msg, addr)
    
    # def update_bot_walls(self):
    #     with self.lock:
    #         players = self.get_players()
    #     walls = self.gameEngine.get_walls()
    #     for player in players:
    #         if player.is_bot():
    #             player.update_walls(walls)


server = Server(server_ip, int(port))
server.run()