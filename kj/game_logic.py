import pygame
from ui import draw_text
import random
import json
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_money = 0
inventory = {"삼각김밥": 0, "컵라면": 0, "도시락": 0}
save_file = "save_data.json"


def beg(money, screen):
    이미지=pygame.image.load("1.jpg")
    이미지=pygame.transform.scale(이미지,(210,500))
    이미지1=pygame.image.load("2.jpg")
    이미지1=pygame.transform.scale(이미지1,(210,500))
    이미지2=pygame.image.load("3.jpg")
    이미지2=pygame.transform.scale(이미지2,(210,500))
    running=True
    screen.fill(WHITE)
    type=0
    touch=0
    fever=0
    start_ticks = pygame.time.get_ticks()
    while running:
        if fever==0 and touch>=50:
            fever=1
            touch=0
            start_ticks = pygame.time.get_ticks()
        if fever==1:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            if elapsed_time>=10:
                fever=0
            touch=0
        screen.fill(WHITE)
        if fever:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            draw_text(screen,f"피버타임 : {str(int(10 - elapsed_time))}초",30,200,70, BLACK)
        if type==1:
            screen.blit(이미지,(300,80))
            draw_text(screen,"히히돈이다",30,200, 120 ,BLACK)
        else:
            if fever:
                screen.blit(이미지2,(300,80))
            else:
                screen.blit(이미지1,(300,80))
            draw_text(screen,"돈주세요",30,200, 120 ,BLACK)
        draw_text(screen, f"현재 자금: {money}원", 30, screen.get_width() // 2, 50, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return money
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    return money
            if event.type == pygame.MOUSEBUTTONDOWN:
                money+=1000
                if fever:
                    money+=1000
                type=1
                touch+=1
            if event.type == pygame.MOUSEBUTTONUP:
                type=0
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
# 주식 정보
stocks = {
    "애플": {"price": 150000, "owned": 0},
    "삼성": {"price": 70000, "owned": 0},
    "테슬라": {"price": 800000, "owned": 0},
}

def start_game(screen):
    global player_money
    running = True
    menu_option = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_option = (menu_option - 1) % 5  # 메뉴 선택
                elif event.key == pygame.K_DOWN:
                    menu_option = (menu_option + 1) % 5
                elif event.key == pygame.K_RETURN:
                    if menu_option == 0:  # 아르바이트
                        player_money = beg(player_money, screen)
                    elif menu_option == 1:  # 편의점
                        player_money = visit_convenience_store(player_money, screen)
                    elif menu_option == 2:  # 주식 구매
                        player_money = trade_stocks(player_money, screen, "buy")
                    elif menu_option == 3:  # 주식 판매
                        player_money = trade_stocks(player_money, screen, "sell")
                    elif menu_option == 4:  # 저장
                        save_game(player_money, inventory)

        screen.fill(WHITE)
        draw_text(screen, "1. 구걸 하기", 30, screen.get_width() // 2, 200, BLACK if menu_option == 0 else (150, 150, 150))
        draw_text(screen, "2. 편의점 가기", 30, screen.get_width() // 2, 250, BLACK if menu_option == 1 else (150, 150, 150))
        draw_text(screen, "3. 주식 구매", 30, screen.get_width() // 2, 300, BLACK if menu_option == 2 else (150, 150, 150))
        draw_text(screen, "4. 주식 판매", 30, screen.get_width() // 2, 350, BLACK if menu_option == 3 else (150, 150, 150))
        draw_text(screen, "5. 저장하기", 30, screen.get_width() // 2, 400, BLACK if menu_option == 4 else (150, 150, 150))
        draw_text(screen, f"현재 자금: {player_money}원", 30, screen.get_width() // 2, 100, BLACK)
        이미지=pygame.image.load("4.jpg")
        이미지=pygame.transform.scale(이미지,(210,500))
        screen.blit(이미지,(600,80))
        draw_text(screen, "즐거워요", 30, 670, 50, BLACK)
        pygame.display.flip()

    return True

# 주식 구매 및 판매
def trade_stocks(money, screen, action):
    global stocks
    menu_option = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return money
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_option = (menu_option - 1) % len(stocks)
                elif event.key == pygame.K_DOWN:
                    menu_option = (menu_option + 1) % len(stocks)
                elif event.key == pygame.K_RETURN:
                    stock_name = list(stocks.keys())[menu_option]
                    stock_price = stocks[stock_name]["price"]

                    if action == "buy" and money >= stock_price:
                        stocks[stock_name]["owned"] += 1
                        money -= stock_price
                        draw_text(screen, f"{stock_name} 주식을 구매했습니다.", 30, screen.get_width() // 2, screen.get_height() // 2, BLACK)
                    elif action == "sell" and stocks[stock_name]["owned"] > 0:
                        stocks[stock_name]["owned"] -= 1
                        money += stock_price
                        draw_text(screen, f"{stock_name} 주식을 판매했습니다.", 30, screen.get_width() // 2, screen.get_height() // 2, BLACK)
                    else:
                        draw_text(screen, "거래 실패", 30, screen.get_width() // 2, screen.get_height() // 2, BLACK)

                    pygame.display.flip()
                    pygame.time.delay(2000)

        screen.fill(WHITE)
        for i, stock in enumerate(stocks.keys()):
            stock_info = stocks[stock]
            draw_text(screen, f"{stock} - 가격: {stock_info['price']}원 / 보유량: {stock_info['owned']}", 30, screen.get_width() // 2, 200 + i * 50, BLACK if menu_option == i else (150, 150, 150))
        draw_text(screen, f"현재 자금: {money}원", 30, screen.get_width() // 2, 100, BLACK)
        pygame.display.flip()
    
    return money

def save_game(money, inventory):
    data = {'money': money, 'inventory': inventory, 'stocks': stocks}
    with open(save_file, 'w') as f:
        json.dump(data, f)
    print(f"게임이 저장되었습니다. (현재 자금: {money}원)")

def load_game():
    global inventory, stocks
    try:
        with open(save_file, 'r') as f:
            data = json.load(f)
        money = data['money']
        inventory = data['inventory']
        stocks = data['stocks']
        print(f"게임이 불러와졌습니다. (불러온 자금: {money}원)")
        return money, inventory
    except FileNotFoundError:
        print("저장된 게임이 없습니다.")
        return 0, {"삼각김밥": 0, "컵라면": 0, "도시락": 0}

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
