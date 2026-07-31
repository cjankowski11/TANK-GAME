import pygame
from menuInfo import MenuInfo
from menu_pages.menuPage import MenuPage
from menu_pages.playPage import PlayPage
from menu_pages.settingsPage import SettingsPage
from menu_pages.localLobbyPage import LocalLobbyPage
from menu_pages.onlineLobbyPage import OnlineLobbyPage
from menu_pages.getNamePage import GetNamePage
import os
from dotenv import load_dotenv
import socket

WIDTH = 800
HEIGHT = 450


class MainMenu:
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.info = MenuInfo()
        self.pages = {}

    def run(self):
        pygame.init()
        self._prepare_pages()
        currentpage = self.pages["MENU"]
        new_page = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.info.online = None
                    self.running = False
                new_page = currentpage.is_page_changed(event)
            if new_page == "QUIT":
                self.running = False
                break
            if new_page == "ONLINE_LOBBY":
                self.pages["ONLINE_LOBBY"].start_connection()
            if new_page:
                currentpage = self.pages[new_page]
            if self.info.game_running:
                self.running = False
                break
            self.screen.fill("purple")
            currentpage.draw_page(self.screen)
            pygame.display.update()
        return self.info

    def _prepare_pages(self):
        load_dotenv()
        server_ip = os.getenv("IP")
        port = os.getenv("PORT")
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        socket_obj.settimeout(7)
        self.pages = {
            "MENU": MenuPage(),
            "SETTINGS": SettingsPage(),
            "PLAY": PlayPage(self.info),
            "LOCAL_LOBBY": LocalLobbyPage(self.info),
            "ONLINE_LOBBY": OnlineLobbyPage(self.info, socket_obj, server_ip, int(port)),
            "GET_NAME": GetNamePage(self.info, socket_obj, server_ip, int(port))
                 }