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
            "ONLINE_LOBBY": OnlineLobbyPage(self.info)
                 }
        currentpage = pages["MENU"]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                new_page = currentpage.is_page_changed(event)
                if new_page == "QUIT":
                    self.running = False
                    break
                if new_page:
                    currentpage = pages[new_page]
            # if self.info.online:
            #     currentpage.send_to_server_msg_that_i_exist()
            self.screen.fill("purple")
            currentpage.draw_page(self.screen)
            pygame.display.update()

