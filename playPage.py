from button import Button
import random

class PlayPage:
    def __init__(self, info):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100, (50, 50, 200), (80, 80, 250), 30)
        self.local_button = Button("LOCAL", 300, 100, 300, 100, (50, 50, 200), (80, 80, 250), 50)
        self.online_button = Button("ONLINE", 300, 250, 300, 100, (50, 50, 200), (80, 80, 250), 50)

    def draw_page(self, screen):
        self.back_button.draw(screen)
        self.local_button.draw(screen)
        self.online_button.draw(screen)


    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            return "MENU"
        if self.local_button.is_clicked(event):
            self.info.online = False
            return "LOCAL_LOBBY"
        if self.online_button.is_clicked(event):
            self.info.online = True
            name = self.get_user_name()
            self.info.name = name
            return "ONLINE_LOBBY"
        return None

    def get_user_name(self):
        return f"Player {random.randint(1000, 10000)}"
