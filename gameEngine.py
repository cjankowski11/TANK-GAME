import pygame
import random
from tank import Tank
import struct

class GameEngine:
    def __init__(self, players_names, game_map):
        self.walls = []
        with open(game_map, "r") as f:
            for line in f:
                wall = line.strip().split(",")
                self.walls.append(pygame.Rect(int(wall[0]), int(wall[1]), int(wall[2]), int(wall[3])))
                self.players = {}
        for name in players_names:
            start_pos = self.get_start_pos(800, 450)
            self.players[name] = Tank(start_pos, random.randint(0, 360), 15)

    def update_player(self, player, sign):
        old_pos = self.players[player].position
        old_angle = self.players[player].angle
        if sign == 0:
            self.players[player].position.y -= 0.05
            #if not does_collide
        elif sign == 2:

            angle = old_angle + 0.02
            if angle > 360:
                angle -= 360
            self.players[player].angle = angle
    def get_players(self, binary=False):
        if binary:
            pass
        return self.players

    def get_walls(self, binary=False):
        if binary:
            buffor = struct.pack("B", len(self.walls))
            for wall in self.walls:
                buffor += struct.pack("<HHHH", wall.left, wall.top, wall.width, wall.height)
            return buffor
        return self.walls
    
    def get_start_pos(self, screen_w, screen_h):
        #tank = pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_1.png").convert_alpha(), 4)
        
        x = random.randint(0, screen_w - 50)
        y = random.randint(0, screen_h - 50)
        return pygame.Vector2(x, y)
    
    def check_collision(self):
        pass
