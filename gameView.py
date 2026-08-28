import pygame
from tank.tankView import TankView
from bullet.BulletView import BulletView

WIDTH = 800
HEIGHT = 450


class GameView:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.walls = []
        self.tanks = {}
        self.tank_images = [
            pygame.transform.scale_by(pygame.image.load(
                "graphics/tank_1/tank_9x9.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load(
                "graphics/tank_2/tank_2_9x9.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load(
                "graphics/tank_3/tank_3_9x9.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load(
                "graphics/tank_4/tank_4_9x9.png").convert_alpha(), 4)
        ]
        self.bullet_images = [pygame.transform.scale_by(
            pygame.image.load("graphics/bullet.png").convert_alpha(), 4)]
        self.bullets = []

    def draw_game(self):
        self.screen.fill("white")
        for wall in self.walls:
            pygame.draw.rect(self.screen, "black", wall)
        for tank in self.tanks.values():
            tank.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        pygame.display.update()
    
    def update_tank(self, name, x, y, angle, bullets, alive):
        self.tanks[name].position.x = x
        self.tanks[name].position.y = y
        self.tanks[name].angle = angle
        self.tanks[name].bullets = bullets
        self.tanks[name].alive = alive

    def update_walls(self, walls):
        self.walls = walls

    def initialize_tanks(self, players):
        for i,  (name, stats) in enumerate(players):
            x, y, angle, bullets = stats
            self.tanks[name] = TankView(pygame.Vector2(x, y), angle,
                                          bullets, self.tank_images[i])
    
    def initialize_tanks_from_tank_engines(self, tanks):
        for i, tank_engine in enumerate(tanks):
            name = tank_engine.player.name
            self.tanks[name] = TankView.from_tank_engine_object(
                        tank_engine, self.tank_images[i])
            
    def update_bullets(self, bullets):
        new_bullets = []
        for bullet in bullets:
            x, y, time = bullet
            new_bullets.append(BulletView(pygame.Vector2(x, y),
                                          time, self.bullet_images[0]))
        self.bullets = new_bullets

    def update_bullets_from_bullet_engine(self, bullets):
        new_bullets = []
        for bullet in bullets:
            x, y, time = bullet.position.x, bullet.position.y, bullet.existence_time
            new_bullets.append(BulletView(pygame.Vector2(x, y),
                                          time, self.bullet_images[0]))
        self.bullets = new_bullets