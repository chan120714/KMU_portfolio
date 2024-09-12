import pygame
import sys
from menu import display_menu
pygame.init()

running=True
font = pygame.font.SysFont("malgungothic", 20)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("박지호인 내가 부자가 될 수 있을리 없잖아, 무리무리! (※무리가 아니었다?)")
def main():
    running = True
    while running:
        running = display_menu(screen)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
