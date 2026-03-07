import pygame


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font_size=30, font_name="ka1.ttf"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(f"graphics/font/{font_name}", font_size)
        
        self._create_text_surface()

    def _create_text_surface(self):
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            return True
        return False
    
    def change_to_sysfont(self, font_name, font_size):
        self.font = pygame.font.SysFont(font_name, font_size)
        self._create_text_surface()