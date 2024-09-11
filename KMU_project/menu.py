import pygame
import sys
from game_logic import start_game

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
font = pygame.font.SysFont("malgungothic", 20)

def display_menu(screen):
    menu_option = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_option = (menu_option - 1) % 2
                elif event.key == pygame.K_DOWN:
                    menu_option = (menu_option + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if menu_option == 0:
                        start_game(screen)
                    elif menu_option == 1:
                        return False

        screen.fill(WHITE)
        draw_menu(screen, menu_option)
        pygame.display.flip()

    return True

def draw_menu(screen, option):
    title_text = font.render("박지호인 내가 부자가 될 수 있을리 없잖아, 무리무리! (※무리가 아니었다?)", True, BLACK)
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))
    
    start_color = BLACK if option == 0 else (150, 150, 150)
    quit_color = BLACK if option == 1 else (150, 150, 150)

    start_text = font.render("[1] 게임 시작", True, start_color)
    screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 200))

    quit_text = font.render("[2] 게임 종료", True, quit_color)
    screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 250))
