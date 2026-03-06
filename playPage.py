from button import Button

class PlayPage:
    def __init__(self):
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
        return None