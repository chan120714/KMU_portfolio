import pygame
import sys
from ui import draw_text
from game_logic import beg,load_game,save_game

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
font = pygame.font.SysFont("malgungothic", 20)

def display_menu(screen):
    menu_option = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            x,y=pygame.mouse.get_pos()
            if screen.get_width() // 2-200 <= x <= screen.get_width() // 2 +200:
                if 200<=y<=240:
                    menu_option = 0
                elif 250<=y<=290:
                    menu_option = 1
                elif 300<=y<=340:
                    menu_option = 2 
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if menu_option == 0:
                        beg(screen)
                    elif menu_option == 1:
                        if load_game()==True:
                            load_game()
                            beg(screen)
                        else:
                            draw_text(screen,"저장된 게임이 없습니다.",20,80,240, BLACK)
                    elif menu_option == 2:
                        return False

        screen.fill(WHITE)
        draw_menu(screen, menu_option)
        pygame.display.flip()

    return True

def draw_menu(screen, option):
    
    pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-200,200,400,40],2)
    pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-200,250,400,40],2)
    pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-200,300,400,40],2)
    title_text = font.render("박지호인 내가 부자가 될 수 있을리 없잖아, 무리무리! (※무리가 아니었다?)", True, BLACK)
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))

    start_text = font.render("[0] 새로운 시작", True, BLACK if option == 0 else (150, 150, 150))
    screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 200))
    
    start_text = font.render("[1] 불러오기", True, BLACK if option == 1 else (150, 150, 150))
    screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 250))
    
    quit_text = font.render("[2] 게임 종료", True, BLACK if option == 2 else (150, 150, 150))
    screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 300))

    draw_text(screen,"© Shin Chan-Young, 2024",15,screen.get_width() // 2 ,560,BLACK)
    draw_text(screen,"Special Thanks to duntakhanalpaca,Park jh",10,screen.get_width() // 2 ,580,BLACK)