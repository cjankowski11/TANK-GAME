import pygame
from gameEngine import GameEngine
from gameView import GameView
from player import Player, BotPlayer
import time

PLAYER_NAMES = ["player1", "player2", "player3", "player4"]


class LocalGame:

    def __init__(self, n_players, n_bots, n_rounds):
        self.ticks_per_sec = 60
        self.number_of_players = n_players
        self.number_of_bots = n_bots
        self.number_of_rounds = n_rounds
        self.players = {}
        for i in range(self.number_of_players):
            self.players[f"{PLAYER_NAMES[i]}"] = (Player(f"{PLAYER_NAMES[i]}"))
        for i in range(self.number_of_bots):
            self.players[f"bot{i}"] = (BotPlayer(f"bot{i}"))

    def players_moves(self):
        keys = pygame.key.get_pressed()
        if self.number_of_players >= 1:
            p1_up, p1_down = keys[pygame.K_w], keys[pygame.K_s]
            p1_left, p1_right = keys[pygame.K_a], keys[pygame.K_d]
            p1_shoot = keys[pygame.K_q]
            self.players[f"{PLAYER_NAMES[0]}"].update(
                p1_up, p1_left, p1_down, p1_right, p1_shoot)
        if self.number_of_players >= 2:
            p2_up, p2_down = keys[pygame.K_i], keys[pygame.K_k]
            p2_left, p2_right = keys[pygame.K_j], keys[pygame.K_l]
            p2_shoot = keys[pygame.K_p]
            self.players[f"{PLAYER_NAMES[1]}"].update(
                p2_up, p2_left, p2_down, p2_right, p2_shoot)
        if self.number_of_players >= 3:
            p3_up, p3_down = keys[pygame.K_UP], keys[pygame.K_DOWN]
            p3_left, p3_right = keys[pygame.K_LEFT], keys[pygame.K_RIGHT]
            p3_shoot = keys[pygame.K_SLASH]
            self.players[f"{PLAYER_NAMES[2]}"].update(
                p3_up, p3_left, p3_down, p3_right, p3_shoot)
        if self.number_of_players >= 4:
            p4_up, p4_down = keys[pygame.K_t], keys[pygame.K_g]
            p4_left, p4_right = keys[pygame.K_f], keys[pygame.K_h]
            p4_shoot = keys[pygame.K_SPACE]
            self.players[f"{PLAYER_NAMES[3]}"].update(
                p4_up, p4_left, p4_down, p4_right, p4_shoot)
            
    def bots_moves(self):
        for player in self.players.values():
            if player.is_bot():
                player.update()

    def run(self):
        tick_duration = 1.0 / self.ticks_per_sec
        for game_round in range(self.number_of_rounds):
            print(f" ROUND: {game_round+1}")
            self.initialize_game()
            self.gameView.draw_game()
            time.sleep(2)
            running = True
            next_tick = time.time()
            while running:
                now = time.time()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        return False
                if now > next_tick:
                    if self.gameEngine.is_finished():
                        running = False
                        self.end_round()
                        break
                    self.game_logic()
                    self.update_view()
                    self.gameView.draw_game()
                    next_tick += tick_duration

    def initialize_game(self):
        self.gameEngine = GameEngine(self.players.values(), self.ticks_per_sec)
        self.gameEngine.choose_map("maps/map1.txt")
        walls = self.gameEngine.get_walls()
        tanks = self.gameEngine.get_tanks()
        self.gameView = GameView()
        self.gameView.update_walls(walls)
        self.gameView.initialize_tanks_from_tank_engines(tanks)
        
    def end_round(self):
        winner = self.gameEngine.get_winner()
        winner.add_point()
        for player in self.players.values():
            print(f"player {player.name} has {player.points} points")

    def game_logic(self):
        self.players_moves()
        self.bots_moves()
        for player in self.players.values():
            instructions = player.get_instructions()
            self.gameEngine.update_tank(
                player, instructions["w"], instructions["a"],
                instructions["s"], instructions["d"], instructions["shoot"])
        self.gameEngine.update_bullets()

    def update_view(self):
        bullets = self.gameEngine.get_bullets()
        self.gameView.update_bullets_from_bullet_engine(bullets)
        tanks = self.gameEngine.get_tanks()
        for tank_engine in tanks:
            name = tank_engine.player.name
            x, y = tank_engine.position.x, tank_engine.position.y
            angle, bullets = tank_engine.angle, tank_engine.bullets_left
            alive = tank_engine.alive
            self.gameView.update_tank(name, x, y, angle, bullets, alive)