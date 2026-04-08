import pygame
from gameEngine import GameEngine
from gameView import GameView


class LocalGame:
    def __init__(self, n_players, n_bots):

        self.number_of_players = n_players
        self.number_of_bots = n_bots
        self.players_names = []
        for i in range(self.number_of_players):
            self.players_names.append(f"player{i}")
        for i in range(self.number_of_bots):
            self.players_names.append(f"bot{i}")


    def player_move(self):
        keys = pygame.key.get_pressed()
        if self.number_of_players >= 1:
            if keys[pygame.K_w]:
                self.gameEngine.update_player("player0", 0)
            if keys[pygame.K_s]:
                self.gameEngine.update_player("player0", 1)
            if keys[pygame.K_a]:
                self.gameEngine.update_player("player0", 2)
            if keys[pygame.K_d]:
                self.gameEngine.update_player("player0", 3)
        if self.number_of_players >= 2:
            if keys[pygame.K_UP]:
                self.gameEngine.update_player("player1", 0)
            if keys[pygame.K_DOWN]:
                print("down")
            if keys[pygame.K_LEFT]:
                print("left")
            if keys[pygame.K_RIGHT]:
                print("right")
        if self.number_of_players >= 3:
            pass
        if self.number_of_players >= 4:
            pass
        for _ in range(self.number_of_bots): #update bot and take his action
            pass
    
    def run(self):
        self.gameEngine = GameEngine(self.players_names, "map1.txt")
        self.gameView = GameView(self.gameEngine.get_walls(), self.gameEngine.get_players())
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
            self.player_move()
            self.gameView.update(self.gameEngine.get_players())
            self.gameView.draw_game()

    