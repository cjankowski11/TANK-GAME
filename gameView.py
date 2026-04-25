import pygame


class GameView:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 450))
        self.walls = []
        self.players = {}
        self.tank_images = [
            pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_1.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_1.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_1.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_1.png").convert_alpha(), 4)
        ]


    def draw_game(self):
        self.screen.fill("white")
        for wall in self.walls:
            pygame.draw.rect(self.screen, "black", wall)
        for i, tank in enumerate(self.players.values()):
            rotated_tank = pygame.transform.rotate(self.tank_images[i], tank.angle)
            new_rect = rotated_tank.get_rect(center=tank.position)
            self.screen.blit(rotated_tank, new_rect)
        pygame.display.update()
    
    def update_player(self, name, x, y, angle, bullets):
        self.players[name].position.x = x
        self.players[name].position.y = y
        self.players[name].angle = angle
        self.players[name].bullets = bullets

    def update_walls(self, walls):
        self.walls = walls

    def initialize_players(self, players):
        self.players = players
