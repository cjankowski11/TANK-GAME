from button import Button
from text import Text
import pygame

class LocalLobbyPage:

    def __init__(self, info):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100, (50, 50, 200), (80, 80, 250), 30)
        add_player = Button("+", 100, 300, 100, 100, (50, 50, 200), (80, 80, 250))
        add_player.change_to_sysfont("arial", 50)
        self.add_player_button = add_player
        sub_player = Button("-", 225, 300, 100, 100, (50, 50, 200), (80, 80, 250))
        sub_player.change_to_sysfont("arial", 50)
        self.subtract_player = sub_player

        self.player_text = Text("PLAYERS", 125, 245)

        add_bot = Button("+", 500, 300, 100, 100, (50, 50, 200), (80, 80, 250))
        add_bot.change_to_sysfont("arial", 50)
        self.add_bot_button = add_bot
        sub_bot = Button("-", 625, 300, 100, 100, (50, 50, 200), (80, 80, 250))
        sub_bot.change_to_sysfont("arial", 50)
        self.subtract_bot = sub_bot

        self.bot_text = Text("BOTS", 550, 245)

    def draw_page(self, screen):
        self.back_button.draw(screen)
        self.add_player_button.draw(screen)
        self.subtract_player.draw(screen)
        self.add_bot_button.draw(screen)
        self.subtract_bot.draw(screen)
        self.player_text.draw(screen)
        self.bot_text.draw(screen)

    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            return "PLAY"
        
        if self.add_player_button.is_clicked(event) and self.info.number_of_players + self.info.number_of_bots < self.info.max_players:
            self.info.number_of_players += 1
            print(f"players {self.info.number_of_players}")
            print(f"bots {self.info.number_of_bots}")
        
        if self.subtract_player.is_clicked(event) and self.info.number_of_players > 0:
            self.info.number_of_players -= 1
            print(f"players {self.info.number_of_players}")
            print(f"bots {self.info.number_of_bots}")

        if self.add_bot_button.is_clicked(event) and self.info.number_of_players + self.info.number_of_bots < self.info.max_players:
            self.info.number_of_bots += 1
            print(f"players {self.info.number_of_players}")
            print(f"bots {self.info.number_of_bots}")
        
        if self.subtract_bot.is_clicked(event) and self.info.number_of_bots > 0:
            self.info.number_of_bots -= 1
            print(f"players {self.info.number_of_players}")
            print(f"bots {self.info.number_of_bots}")
