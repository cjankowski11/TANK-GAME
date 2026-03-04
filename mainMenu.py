import pygame
from button import Button

class MainMenu:
    def __init__(self):
        self.height = 450
        self.width = 800
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        pygame.init()
        play_button = Button("PLAY", 225, 50, 350, 100, (50, 50, 200), (80, 80, 250), 50)
        settings_button = Button("SETTINGS", 225, 175, 350, 100, (50, 50, 200), (80, 80, 250), 50)
        quit_button = Button("QUIT", 225, 300, 350, 100, (50, 50, 200), (80, 80, 250), 50)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or quit_button.is_clicked(event):
                    self.running = False
            self.screen.fill("purple")
            play_button.draw(self.screen)
            settings_button.draw(self.screen)
            quit_button.draw(self.screen)
            pygame.display.update()

