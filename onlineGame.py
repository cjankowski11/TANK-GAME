import socket
import threading
import struct
import pygame
import time
from gameView import GameView
from player import Player
import network_constants as nc


class OnlineGame:
    def __init__(self, socket, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.socket = socket
        self.gameView = None
        self.running = True
        self.player = Player()

    def update(self):
        pass
    
    def run(self):
        self.gameView = GameView()
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
        
            keys = pygame.key.get_pressed()
            w = keys[pygame.K_w]
            a = keys[pygame.K_a]
            s = keys[pygame.K_s]
            d = keys[pygame.K_d]
            shoot = keys[pygame.K_SPACE]
            self.player.update(w, a, s, d, shoot)
            
            self.gameView.draw_game()
        
    def listener(self):
        actions = {
            nc.STARTING_WALLS_AND_PLAYERS: self.initialize_map,
            nc.PLAYERS_AND_BULLETS: self.update_game,
            nc.END_GAME: self.game_finished
        }
        while self.running:
            try:
                msg, _ = self.socket.recvfrom(2048)
                number = msg[0]
                print(number)
                actions[number](msg)

            except socket.timeout:
                continue
            # except Exception as e:
            #     print(e)
            # time.sleep(0.01)
    
    def broadcasting(self):
        while self.running:
            instructions = self.player.get_instructions()
            msg = struct.pack(
                "BBBBBB", nc.PLAYER_INSTRUCTIONS,
                instructions["w"], instructions["a"], instructions["s"],
                instructions["d"], instructions["shoot"])
            # try:
            self.socket.sendto(msg, (self.host, self.port))
            # except Exception as e:
            #     print(e)
            time.sleep(0.01)
    
    def start_connection(self):
        threading.Thread(target=self.listener, daemon=True).start()
        threading.Thread(target=self.broadcasting, daemon=True).start()

    def initialize_map(self, msg):
        print("initialize")
        number_of_walls = msg[1]
        offset = 2
        walls = []
        tanks = {}
        for _ in range(number_of_walls):
            left, top, width, height = struct.unpack(
                "<HHHH", msg[offset:offset+8])
            walls.append(pygame.Rect(left, top, width, height))
            offset += 8
        number_of_tanks = msg[offset]
        offset += 1
       
        for _ in range(number_of_tanks):
            name_length = struct.unpack("B", msg[offset:offset+1])[0]
            offset += 1
            name = struct.unpack(
                f"{name_length}s", msg[offset:offset+name_length])[0]
            name = name.decode()
            offset += name_length
            x, y, angle, bullets = struct.unpack("fffB", msg[offset:offset+13])
            offset += 13
            tanks[name] = (x, y, angle, bullets)
        print(tanks)
        self.gameView.update_walls(walls)
        self.gameView.initialize_tanks(tanks)
        self.gameView.update_bullets([])
        
    def update_game(self, msg):
        number_of_players = msg[1]
        offset = 2
        for _ in range(number_of_players):
            name_length = struct.unpack("B", msg[offset:offset+1])[0]
            offset += 1
            name = struct.unpack(
                f"{name_length}s", msg[offset:offset+name_length])[0]
            name = name.decode()
            offset += name_length
            x, y, angle, bullets = struct.unpack("fffB", msg[offset:offset+13])
            offset += 13
            self.gameView.update_player(name, x, y, angle, bullets, True)
        number_of_bullets = msg[offset]

        offset += 1
        bullets = []
        for _ in range(number_of_bullets):
            x, y, time_of_existence = struct.unpack(
                "ffH", msg[offset:offset+10])
            offset += 10
            bullets.append((x, y, time_of_existence))
        self.gameView.update_bullets(bullets)
    
    def game_finished(self, msg):
        self.running = False

    def is_game_finished(self):
        return not self.running
    




