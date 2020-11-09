import pygame

class Text:
    def __init__(self):
        pass
    def draw_text(self, surf,text, x, y, size):
        font_name = pygame.font.match_font('arial')
        render_font = pygame.font.Font(font_name, size)
        render_text = render_font.render(text, True, (255,255,255))
        text_rect = render_text.get_rect()

        text_rect.x, text_rect.y = (x, y)
        surf.blit(render_text, text_rect)