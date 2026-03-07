from button import Button


class MenuPage:

    def __init__(self):
        self.play_button = Button("PLAY", 225, 50, 350, 100, (50, 50, 200), (80, 80, 250), 50)
        self.settings_button = Button("SETTINGS", 225, 175, 350, 100, (50, 50, 200), (80, 80, 250), 50)
        self.quit_button = Button("QUIT", 225, 300, 350, 100, (50, 50, 200), (80, 80, 250), 50)
    
    def draw_page(self, screen):
        self.play_button.draw(screen)
        self.settings_button.draw(screen)
        self.quit_button.draw(screen)
    
    def is_page_changed(self, event):
        if self.play_button.is_clicked(event):
            return "PLAY"
        if self.settings_button.is_clicked(event):
            return "SETTINGS"
        if self.quit_button.is_clicked(event):
            return "QUIT"
        return None
