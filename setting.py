import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 창 제목 설정
pygame.display.set_caption("박지호인 내가 부자가 될 수 있을리 없잖아, 무리무리! (※무리가 아니었다?)")

# 기본 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 폰트 설정 (텍스트 표시를 위해)
font = pygame.font.Font(None, 36)

# 게임 루프를 위한 변수
running = True
font = pygame.font.SysFont("malgungothic", 20)

# 기본 게임 루프
while running:
    screen.fill(WHITE)  # 배경을 흰색으로 채움
    
    # 이벤트 처리 (게임 종료)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    title_text = font.render("박지호인 내가 부자가 될 수 있을리 없잖아, 무리무리! (※무리가 아니었다?) ", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
    
    start_text = font.render("[1] 게임 시작", True, BLACK)
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 200))
    
    quit_text = font.render("[2] 게임 종료", True, BLACK)
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 250))
    
    # 화면 업데이트
    pygame.display.flip()

# 게임 종료 처리
pygame.quit()
sys.exit()
