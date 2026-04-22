import socket
import threading
import time
import struct
from gameEngine import GameEngine
from dotenv import load_dotenv
import os
load_dotenv()
server_ip = os.getenv("IP")
port = os.getenv("PORT")


class Server:
    def __init__(self, host='127.0.0.1', port=34567):
        self.host = host
        self.port = port
        self.start_game = False
        self.kill = False
        self.thread_count = 0
        self.menu_players = {}
        self.max_players = 4
        self.bots_number = 0
        self.rounds_number = 5
        self.players_addr_name = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(1)
        self.lock = threading.Lock()

    def handle_data(self, data, addr):
        try:
            if len(data):
                msg_type = struct.unpack("B", data[:1])[0]
                now = time.time()
                decoded_name = None
                ready_status = False
                if msg_type == 1:
                    ready_status, name_raw = struct.unpack("?20s", data[1:])
                    decoded_name = name_raw.decode().strip('\x00')
                with self.lock:
                    if addr in self.menu_players:
                        self.menu_players[addr]["time"] = now
                
                    if msg_type == 1:        
                        all_players = self.get_menu_players_number() + self.bots_number
                        addrs = self.get_menu_players_addrs()
                        if all_players < 4 or addr in addrs:
                            self.menu_players[addr] = {"name": decoded_name,
                                                       "time": now,
                                                       "ready": ready_status}

                    elif msg_type == 2:
                        if self.bots_number + self.get_menu_players_number() < 4:
                            self.bots_number += 1

                    elif msg_type == 3:
                        if self.bots_number > 0:
                            self.bots_number -= 1

                    elif msg_type == 4 and not self.start_game:
                        self.start_game = (bool(self.menu_players) and
                                           all(p["ready"]
                                           for p in self.menu_players.values()))
                    elif msg_type == 5:
                        if self.rounds_number < 20:
                            self.rounds_number += 1
                    
                    elif msg_type == 6:
                        if self.rounds_number > 1:
                            self.rounds_number -= 1
                        
        except Exception as e:
            print(f"error {e}")

    def listen_loop(self):
        self.thread_count += 1
        print("Server working")
        while not self.kill:
            try:
                data, addr = self.socket.recvfrom(2048)
                self.handle_data(data, addr)   # handle_menu_data and handle game_data
            except socket.timeout:
                continue
            except Exception as e:
                print(e)
            # time.sleep(0.01)
        self.thread_count -= 1

    def broadcasting(self):
        game_initialized = False
        ticks_per_sec = 60

        self.thread_count += 1

        while not self.kill:
            next_tick = time.time()
            with self.lock:
                active_game = self.start_game
                current_players = list(self.menu_players.keys())
            now = time.time()
            # print(active_game)
            if not active_game:
                self.resending_active_players()
            else:
                if not game_initialized:   #make sure that client gets start message before data
                    self.initialize_game() # imo client sends info that he got start info
                    for addr in current_players:      #nvm najlepiej po prostu sygnal kilka razy wyslac bo czekanie moze byc problematyczne jak kogos wyjebie
                        self.socket.sendto(struct.pack("B", 1), addr)
                    game_initialized = True
                    time.sleep(0.1)
                    for _ in range(5):
                        self.send_starting_info()
                        time.sleep(0.5)

                if now >= next_tick:
                    self.update_game_logic()  
                    self.broadcast_game_state() 
                    next_tick += 1.0 / ticks_per_sec
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
                
        except KeyboardInterrupt:
            self.await_kill()

    
    def delete_not_active(self):
        addr_to_delete = []
        for addr, _ in self.menu_players.items():
            if time.time() - self.menu_players[addr]["time"] > 5:
                addr_to_delete.append(addr)
        for addr in addr_to_delete:
            self.menu_players.pop(addr)

    def get_menu_players_number(self):
        return len(self.menu_players)
    
    def get_menu_players_addrs(self):
        return list(self.menu_players.keys())

    def get_menu_players_values(self):
        return list(self.menu_players.values())
    
    def resending_active_players(self):
        with self.lock:
            self.delete_not_active()
            current_players = self.get_menu_players_values()
            num_players = self.get_menu_players_number()
            current_bots = self.bots_number
            rounds = self.rounds_number
        buffor = struct.pack("BBBB", 0, num_players, current_bots, rounds)
        for value in current_players:
            buffor += struct.pack("?20s", value["ready"], (value["name"]).encode())
        with self.lock:
            addrs = self.get_menu_players_addrs()

        for addr in addrs:
            try:
                self.socket.sendto(buffor, addr)
            except Exception as e:
                print(e)
            
    def initialize_game(self): 
        with self.lock:
            names = [value["name"] for value in self.menu_players.values()]
            for i in range(self.bots_number):
                names.append(f"BOT{i}")
            for player, value in self.menu_players.items(): # is it needed? ig not
                self.players_addr_name[player] = value["name"]
        self.gameEngine = GameEngine(names, "map1.txt")
                


    def update_game_logic(self):
        pass

    def broadcast_game_state(self):
        pass

    def send_starting_info(self):
        # send walls to players
        walls = self.gameEngine.get_walls(binary=True)
        players = self.gameEngine.get_players(binary=True)
        msg = struct.pack("B", 2) + walls + players
        print(msg)
        with self.lock:
            addrs = self.get_menu_players_addrs()
        for addr in addrs:
            self.socket.sendto(msg, addr)

server = Server(server_ip, int(port))
server.run()