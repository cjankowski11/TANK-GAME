import socket
import threading
import struct
import pygame
import random
import math
import time
from gameView import GameView


class OnlineGame:
    def __init__(self, bots_number, rounds_number, socket, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.rounds = rounds_number
        self.socket = socket
        self.gameView = None

    def update(self):
        pass
    
    def run(self):
        self.gameView = GameView([], [])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
            self.gameView.draw_game()
        

    def listener(self):
        actions = {
            2: self.update_walls
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
        pass

    def start_connection(self):
        threading.Thread(target=self.listener, daemon=True).start()
        threading.Thread(target=self.broadcasting, daemon=True).start()

    def update_walls(self, msg):
        number_of_walls = msg[1]
        msg = msg[2:]
        walls = []
        for _ in range(number_of_walls):
            left, top, width, height = struct.unpack("HHHH", msg[:8])
            msg = msg[8:]
            walls.append(pygame.Rect(left, top, width, height))
        self.gameView.update_walls(walls)



