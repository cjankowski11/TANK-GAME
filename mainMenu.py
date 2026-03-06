import pygame
from menuInfo import MenuInfo
from menuPage import MenuPage
from playPage import PlayPage
class MainMenu:
    def __init__(self):
        self.height = 450
        self.width = 800
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.info = MenuInfo()

    def run(self):
        pygame.init()
        pages = {
            "MENU": MenuPage(),
            "SETTINGS": "",
            "PLAY": PlayPage()
                 }
        currentpage = pages["MENU"]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                change = currentpage.is_page_changed(event)
                if change == "QUIT":
                    self.running = False
                    break
                if change:
                    currentpage = pages[change]
            self.screen.fill("purple")
            currentpage.draw_page(self.screen)
            pygame.display.update()

