import socket
import threading
import struct
import pygame
import random
WIDTH = 800
HEIGHT = 450


class Game:
    def __init__(self, host="localhost", port=48889):
        self.host = host
        self.port = port
        self.kill = False
        self.running = True
        self.socket = None
        pygame.init()
        pygame.display.set_mode((WIDTH, HEIGHT))
        self.czolg_1_pos = pygame.Vector2(random.randint(0, WIDTH), (random.randint(0, HEIGHT)))
        self.czolg_1 = pygame.transform.scale_by(pygame.image.load("graphics/czolg_1/czolg_1.png"), 2)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.czolg_1_pos.y -= 0.01
        self.screen.fill("white")
        self.screen.blit(self.czolg_1, self.czolg_1_pos)
        pygame.display.update()

    def run(self):
        threading.Thread(target=self.run_listener).start()
        while self.running:
            self.update()
        pygame.quit()
    
    def run_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.connect((self.host, self.port))
            # tutaj jedna linika kodu w wtutorialu ale do tcp
            s.settimeout(1)
            print(f"connected {s}")
            self.socket = s



