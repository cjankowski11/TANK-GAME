import socket
import threading
import struct
import pygame
import random
import math
import time



class Game:
    def __init__(self, host="127.0.0.1", port=48889):
        self.host = host
        self.port = port
        self.running = True
        self.socket = None
        self.online = False  #ewentualnie mozna zastapic socket
        
        # pygame.display.set_mode((WIDTH, HEIGHT))
        # self.czolg_1_pos = pygame.Vector2(random.randint(0, WIDTH), (random.randint(0, HEIGHT)))
        # self.czolg_1 = pygame.transform.scale_by(pygame.image.load("graphics/czolg_1/czolg_1.png").convert_alpha(), 2)
        
        # self.angle = 0
        # self.speed = 0.02
    def draw_page(self, screen):
        screen.fill("white")

    def is_page_changed(self, event):
        pass

    def main_menu(self):
        main_menu_loop = True
        while main_menu_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_menu_loop = False
            self.screen.fill("purple")
            pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            # self.czolg_1_pos.y -= 0.02
            # self.czolg_1_pos.x -= math.cos(self.angle)*self.speed
            # self.czolg_1_pos.y += math.sin(self.angle)*self.speed
            self.socket.sendto(b"w", (self.host, self.port))
        if keys[pygame.K_s]:
            self.socket.sendto(b"s", (self.host, self.port))
        if keys[pygame.K_a]:
            # self.angle += 0.05
            # if self.angle > 360:
            #     self.angle -= 360
            pass
        if keys[pygame.K_d]:
            # self.angle -= 0.05
            # if self.angle < 0:
            #     self.angle += 360
            pass

        rotated = pygame.transform.rotate(self.czolg_1, self.angle)
        self.screen.fill("white")
        self.screen.blit(rotated, self.czolg_1_pos)
        pygame.display.update()

    def window_closing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.online:
                self.s.sendto(b"siadla mu psycha")
    def run(self):
        # threading.Thread(target=self.run_listener).start()
        self.main_menu()
        while self.running:
            self.update()
        pygame.quit()

    def deserialize(self, data):
        pass

    def run_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            # s.connect((self.host, self.port))
            # tutaj jedna linika kodu w wtutorialu ale do tcp
            s.settimeout(1)
            print(f"connected {s}")
            self.socket = s
            while self.running:
                try:
                    # data = self.socket.recv(2048)
                    # if len(data):
                    #     self.deserialize(data)
                    pass
                except socket.timeout:
                    pass
                time.sleep(0.001)
            



