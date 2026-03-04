import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        # self.font = pygame.font.SysFont("ubuntumono", font_size)
        self.font = pygame.font.Font("graphics/font/ka1.ttf", font_size)
        
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=12)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            return True
        return False