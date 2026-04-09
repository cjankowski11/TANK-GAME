import pygame
from menuInfo import MenuInfo
from menuPage import MenuPage
from playPage import PlayPage
from settingsPage import SettingsPage
from localLobbyPage import LocalLobbyPage
from onlineLobbyPage import OnlineLobbyPage


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
            "SETTINGS": SettingsPage(),
            "PLAY": PlayPage(self.info),
            "LOCAL_LOBBY": LocalLobbyPage(self.info),
            "ONLINE_LOBBY": OnlineLobbyPage(self.info, ),
                 }
        currentpage = pages["MENU"]
        new_page = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                new_page = currentpage.is_page_changed(event)
            if new_page == "QUIT":
                self.running = False
                break
            if new_page == "ONLINE_LOBBY":
                pages["ONLINE_LOBBY"].start_connection()
            if new_page:
                currentpage = pages[new_page]

            if self.info.game_running:
                self.running = False
                break
            self.screen.fill("purple")
            currentpage.draw_page(self.screen)
            pygame.display.update()
        return self.info

        