import pygame
import random
from tank.tankEngine import TankEngine
import struct
import math

WIDTH = 800
HEIGHT = 450
TANK_MAX_AMUNITION = 8
TANK_SPEED = 60
TANK_TURN_SPEED = 120
BULLET_SPEED = 90


class GameEngine:
    def __init__(self, players_names, ticks_per_sec):
        self.ticks_per_sec = ticks_per_sec
        self.walls = []
        self.players = {}
        self.players_names = players_names
        self.bullets = []
        self.game_over = False
        self.choose_map()

    def is_finished(self):
        alive_count = 0
        for tank in self.players.values():
            if tank.is_alive():
                alive_count += 1
        if alive_count < 2:
            self.game_over = True
            return True
        else:
            return False

    def update_player(self, player, w, a, s, d, shoot):
        tank = self.players[player]
        if not tank.is_alive():
            return False
        old_angle = tank.angle
        old_pos = tank.position.copy()

        if self.check_tank_bullets_collision(tank):
            tank.alive = False

        tank.update_reload_cooldown()
        tank.update_shoot_cooldown()

        if tank.is_able_to_reload():
            tank.reload_bullet()
        if a:
            tank.angle += TANK_TURN_SPEED/self.ticks_per_sec
        if d:
            tank.angle -= TANK_TURN_SPEED/self.ticks_per_sec

        tank.angle %= 360

        if self.check_collision(tank):
            tank.angle = old_angle 

        move_x = 0
        move_y = 0
        rad = math.radians(tank.angle)

        if w:
            move_x -= math.sin(rad)
            move_y -= math.cos(rad)
        if s:
            move_x += math.sin(rad)
            move_y += math.cos(rad)

        tank.position.x += move_x*TANK_SPEED/self.ticks_per_sec
        if self.check_collision(tank):
            tank.position.x = old_pos.x 

        tank.position.y += move_y*TANK_SPEED/self.ticks_per_sec
        if self.check_collision(tank):
            tank.position.y = old_pos.y 

        if shoot and tank.is_able_to_shoot():
            bullet = tank.shoot()
            self.bullets.append(bullet)

    def update_bullets(self):
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.update_exist_time()
            if not bullet.is_existing() or self.check_bullet_walls_collision(bullet):
                bullets_to_remove.append(bullet)
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
        
        for bullet in self.bullets:
            rad = math.radians(bullet.angle)
            bullet.position.x -= math.sin(rad)*BULLET_SPEED/self.ticks_per_sec
            bullet.position.y -= math.cos(rad)*BULLET_SPEED/self.ticks_per_sec

    def get_players(self, binary=False):
        if binary:
            buffor = struct.pack("B", len(self.players))
            for name, tank in self.players.items():
                name = name.encode()
                name_length = len(name)
                buffor += struct.pack(f"B{name_length}s", name_length, name)
                buffor += struct.pack("fffB", tank.position.x, tank.position.y,
                                      tank.angle, tank.bullets_left)
            return buffor
        return self.players

    def get_walls(self, binary=False):
        if binary:
            buffor = struct.pack("B", len(self.walls))
            for wall in self.walls:
                buffor += struct.pack("<HHHH", wall.left, wall.top, wall.width,
                                      wall.height)
            return buffor
        return self.walls
    
    def get_start_pos(self, screen_w, screen_h):
        while True:
            x = random.randint(50, screen_w - 50)
            y = random.randint(100, screen_h - 100)
            if not self.check_starting_collision(x, y):
                return pygame.Vector2(x, y)

    
    def get_bullets(self, binary=False):
        if binary:
            buffor = struct.pack("B", len(self.bullets))
            for bullet in self.bullets:
                buffor += struct.pack("ffH", bullet.position.x,
                                      bullet.position.y, bullet.existence_time)
            return buffor
        return self.bullets
    
    def check_starting_collision(self, x, y):
        tank_rect = pygame.Rect(0, 0, 20, 20)
        tank_rect.center = (int(x), int(y))
        for wall in self.walls:
            if wall.colliderect(tank_rect):
                return True
        return False


    def check_collision(self, tank):
        tank_rect = pygame.Rect(0, 0, 20, 20)
        tank_rect.center = (int(tank.position.x), int(tank.position.y))

        for wall in self.walls:
            if wall.colliderect(tank_rect):
                return True
        return False
    
    def check_bullet_walls_collision(self, bullet):
        bullet_rect = pygame.Rect(0, 0, 5, 5)
        bullet_rect.center = (int(bullet.position.x), int(bullet.position.y))
        for wall in self.walls:
            if wall.colliderect(bullet_rect):
                return True
        return False
    
    def check_tank_bullets_collision(self, tank):
        tank_rect = pygame.Rect(0, 0, 20, 20)
        tank_rect.center = (int(tank.position.x), int(tank.position.y))
        for bullet in self.bullets:
            bullet_rect = pygame.Rect(0, 0, 5, 5)
            bullet_rect.center = (int(bullet.position.x), int(bullet.position.y))
            if tank_rect.colliderect(bullet_rect):
                return True
        return False
    
    def get_winner(self):
        winner = None
        if self.game_over:
            for player, tank in self.players.items():
                if tank.is_alive():
                    winner = player
        return winner
    
    def choose_map(self, map_filename=None):
        self.walls = []
        maps = ["maps/map1.txt", "maps/map2.txt", "maps/map3.txt"]
        if map_filename is None:
            map_filename = random.choice(maps)
        with open(map_filename, "r") as f:
            for line in f:
                wall = line.strip().split(",")
                self.walls.append(pygame.Rect(int(wall[0]), int(wall[1]),
                                              int(wall[2]), int(wall[3])))
        self.generate_players_on_map()

    def generate_players_on_map(self):
        for name in self.players_names:
            start_pos = self.get_start_pos(WIDTH, HEIGHT)
            self.players[name] = TankEngine(start_pos, random.randint(0, 360),
                                            TANK_MAX_AMUNITION, self.ticks_per_sec)

    def reset(self):
        self.bullets = []
        self.choose_map()

