import pygame


class Text:
    def __init__(self, text, x, y, color=(255, 255, 255), font_name="ka1.ttf", font_size=30):
        self.pos = (x, y)
        self.font = pygame.font.Font(f"graphics/font/{font_name}", font_size)
        
        self.text_surf = self.font.render(text, True, color)

    def draw(self, screen):
        screen.blit(self.text_surf, self.pos)