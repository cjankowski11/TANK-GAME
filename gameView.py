import pygame


class GameView:
    def __init__(self, walls, players):
        self.screen = pygame.display.set_mode((800, 450))
        self.walls = walls
        self.players = players
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
        for i, player in enumerate(self.players):
            self.screen.blit(self.tank_images[i], self.players[player].position)
        pygame.display.update()
    
    def update(self, players):
        self.players = players

    def update_walls(self, walls):
        self.walls = walls
