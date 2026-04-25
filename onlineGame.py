import socket
import threading
import struct
import pygame
import random
import math
import time
from tank import Tank
from gameView import GameView
import queue

class OnlineGame:
    def __init__(self, bots_number, rounds_number, socket, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.rounds = rounds_number
        self.socket = socket
        self.gameView = None
        self.action_queue = queue.Queue()

    def update(self):
        pass
    
    def run(self):
        self.gameView = GameView()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("shoot")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.action_queue.put(0)
            if keys[pygame.K_s]:
                self.action_queue.put(2)

                
            
            self.gameView.draw_game()
        

    def listener(self):
        actions = {
            2: self.initialize_map,
            3: self.update_game
        }
        while True:
            try:
                msg, _ = self.socket.recvfrom(2048)
                
                number = msg[0]
                actions[number](msg)

            except socket.timeout:
                continue
            except Exception as e:
                print(e)
            time.sleep(0.01)
    
    def broadcasting(self):
        while True:
            msg = struct.pack("B", 7)
            
            data = struct.pack("B", self.action_queue.get()) 
            i = 1 
            while not self.action_queue.empty() and i < 50:
                try:
                    data += struct.pack("B", self.action_queue.get_nowait())
                    i += 1
                except queue.Empty:
                    break
            msg += struct.pack("B", i)
            msg += data
            try:
                self.socket.sendto(msg, (self.host, self.port))
            except Exception as e:
                print(e)
    


    def start_connection(self):
        threading.Thread(target=self.listener, daemon=True).start()
        threading.Thread(target=self.broadcasting, daemon=True).start()

    def initialize_map(self, msg):
        
        number_of_walls = msg[1]
        offset = 2
        walls = []
        players = {}
        for _ in range(number_of_walls):
            left, top, width, height = struct.unpack("<HHHH", msg[offset:offset+8])
            walls.append(pygame.Rect(left, top, width, height))
            offset += 8
        number_of_players = msg[offset]
        offset += 1
        print(number_of_players)
        for _ in range(number_of_players):
            name = struct.unpack("20s", msg[offset:offset+20])
            print(name)
            offset += 20
            x, y, angle, bullets = struct.unpack("fffB", msg[offset:offset+13])
            print(x, y, angle)
            offset += 13
            players[name] = Tank(pygame.Vector2(x, y), angle, bullets)
        self.gameView.update_walls(walls)
        self.gameView.initialize_players(players)
    
    def update_game(self, msg):
        number_of_players = msg[1]
        offset = 2
        for _ in range(number_of_players):
            name = struct.unpack("20s", msg[offset:offset+20])
            print(name)
            offset += 20
            x, y, angle, bullets = struct.unpack("fffB", msg[offset:offset+13])
            print(x, y, angle)
            offset += 13
            self.gameView.update_player(name, x, y, angle, bullets)




