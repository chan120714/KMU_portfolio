import pygame

def draw_text(screen, text, size, x, y, color):
    font = pygame.font.SysFont("malgungothic", size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))
