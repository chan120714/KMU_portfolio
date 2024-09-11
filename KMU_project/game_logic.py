import pygame
from ui import draw_text
import random
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_money = 0
inventory = {"삼각김밥": 0, "컵라면": 0, "도시락": 0}
save_file = "save_data.json"

def start_game(screen):
    global player_money,inventory
    running = True
    menu_option = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_option = (menu_option - 1) % 4  # 메뉴 선택
                elif event.key == pygame.K_DOWN:
                    menu_option = (menu_option + 1) % 4
                elif event.key == pygame.K_RETURN:
                    if menu_option == 0:  # 아르바이트
                        player_money = do_part_time_job(player_money, screen)
                    elif menu_option == 1:  # 편의점
                        player_money = visit_convenience_store(player_money, screen)
                    elif menu_option == 2:  # 저장
                        save_game(player_money, inventory)
                    elif menu_option == 3:  # 불러오기
                        player_money, inventory = load_game()

        screen.fill(WHITE)
        draw_text(screen, "1. 아르바이트 하기", 30, screen.get_width() // 2, 200, BLACK if menu_option == 0 else (150, 150, 150))
        draw_text(screen, "2. 편의점 가기", 30, screen.get_width() // 2, 250, BLACK if menu_option == 1 else (150, 150, 150))
        draw_text(screen, "3. 저장하기", 30, screen.get_width() // 2, 300, BLACK if menu_option == 2 else (150, 150, 150))
        draw_text(screen, "4. 불러오기", 30, screen.get_width() // 2, 350, BLACK if menu_option == 3 else (150, 150, 150))
        draw_text(screen, f"현재 자금: {player_money}원", 30, screen.get_width() // 2, 100, BLACK)

        pygame.display.flip()

    return True

def do_part_time_job(money, screen):
    target_text = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(5,15)))
    typed_text = ''
    earnings = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return money
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                else:
                    typed_text += event.unicode

        screen.fill(WHITE)
        draw_text(screen, f"타자 연습: {target_text}", 30, screen.get_width() // 2, 200, BLACK)
        draw_text(screen, f"입력한 글자: {typed_text}", 30, screen.get_width() // 2, 250, BLACK)

        if typed_text == target_text:
            earnings = len(target_text) * 1000
            money += earnings
            draw_text(screen, f"아르바이트 완료! +{earnings}원 획득", 30, screen.get_width() // 2, screen.get_height() // 2, BLACK)
            pygame.display.flip()
            pygame.time.delay(500)
            running = False

        pygame.display.flip()
    
    return money

def visit_convenience_store(money, screen):
    global inventory
    items = [("삼각김밥", 1500), ("컵라면", 1000), ("도시락", 4500)]
    menu_option = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return money
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_option = (menu_option - 1) % (len(items)+1)
                elif event.key == pygame.K_DOWN:
                    menu_option = (menu_option + 1) % (len(items)+1)
                elif event.key == pygame.K_RETURN:
                    if menu_option == len(items):
                        running = False
                        break
                    item, price = items[menu_option]
                    if money >= price:
                        money -= price
                        inventory[item] += 1
                    else:
                        draw_text(screen, "돈이 부족합니다.", 30, screen.get_width()//2, screen.get_height()//2+90, BLACK)
                        pygame.display.flip()
                        pygame.time.delay(500)

        screen.fill(WHITE)
        for i, (item, price) in enumerate(items):
            draw_text(screen, f"{item} - {price}원 ({inventory[item]}개 소지중)", 30, screen.get_width() // 2, 200 + i * 50, BLACK if menu_option == i else (150, 150, 150))
        draw_text(screen, f"4 - 나가기", 30, screen.get_width() // 2,350, BLACK if menu_option==3 else (150, 150, 150))
        draw_text(screen, f"현재 자금: {money}원", 30, screen.get_width() // 2, 100, BLACK)
        pygame.display.flip()
    
    return money

def save_game(money, inventory):
    data = {'money': money, 'inventory': inventory}
    with open(save_file, 'w') as f:
        json.dump(data, f)
    print(f"게임이 저장되었습니다. (현재 자금: {money}원)")

def load_game():
    global inventory
    try:
        with open(save_file, 'r') as f:
            data = json.load(f)
        money = data['money']
        inventory = data['inventory']
        print(f"게임이 불러와졌습니다. (불러온 자금: {money}원)")
        return money, inventory
    except FileNotFoundError:
        print("저장된 게임이 없습니다.")
        return 0, {"삼각김밥": 0, "컵라면": 0, "도시락": 0}
