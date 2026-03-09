import pygame


class Text:
    def __init__(self, text, x, y, color=(255, 255, 255), font_name="ka1.ttf", font_size=30):
        self.pos = (x, y)
        self.font = pygame.font.Font(f"graphics/font/{font_name}", font_size)
        self.color = color
        self.text_surf = self.font.render(text, True, color)
        self.visible = True
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.text_surf, self.pos)

    def change_text(self, new_text):
        self.text_surf = self.font.render(new_text, True, self.color)