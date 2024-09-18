import pygame
from ui import draw_text
import random
import json
from math import *
import os
import sys

def resource_path(relative_path):
    try:
        # PyInstaller로 실행된 경우
        base_path = sys._MEIPASS
    except AttributeError:
        # 개발 환경에서 실행된 경우
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_money = 0
touch_money = 1
plus_percent = 100
level=1
cost=10
reincarnate=0
inventory = {"김채원의 굿즈":0, "알파카의 캡슐커피":0, "김종말의 다이어트 용품":0, "한지호의 마블굿즈":0,"신희후의 노트북":0,"김수인의 코스프레 용품":0,
             "심유묘 박주환":0, "코스프레남 이승민":0, "허수 최우혁":0, "허리디스크 조준익":0, "그냥 김민학":0, "박경준":0, "게임폐인 김인우":0, "철학과 이준호":0}
save_file = resource_path("save_data.json")
beg_probability=10
reincarnate_plus_percent=0
def level_up():
    global level
    global cost
    global touch_money
    level+=1
    if level>200:
        touch_money+=level
    touch_money+=level
    cost*=1.05
    cost=ceil(cost)


def beg(screen):
    global beg_probability,plus_percent,player_money
    이미지=pygame.image.load(resource_path('assets/1.jpg'));이미지=pygame.transform.scale(이미지,(210,500))
    이미지1=pygame.image.load(resource_path('assets/2.jpg'));이미지1=pygame.transform.scale(이미지1,(210,500))
    이미지2=pygame.image.load(resource_path('assets/3.jpg'));이미지2=pygame.transform.scale(이미지2,(210,500))
    이미지5=pygame.image.load(resource_path('assets/5.jpg'));이미지5=pygame.transform.scale(이미지5,(210,500))
    이미지4=pygame.image.load(resource_path('assets/4.jpg'));이미지4=pygame.transform.scale(이미지4,(210,500))
    running=True
    screen.fill(WHITE)
    type=0
    touch=0
    fever=0
    is_money=1
    start_ticks = pygame.time.get_ticks()
    while running:
        save_game()
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
        pygame.draw.rect(screen,BLACK,[500,80,250,80],2)
        pygame.draw.rect(screen,BLACK,[500,200,250,80],2)
        pygame.draw.rect(screen,BLACK,[500,300,250,80],2)
        pygame.draw.rect(screen,BLACK,[500,400,250,80],2)
        draw_text(screen,f"현재 구걸 성공확률 : {beg_probability}% ",20,80,200, BLACK)
        draw_text(screen,f"현재 추가금액: {plus_percent-100}% ",20,100,240, BLACK)
        draw_text(screen,f"박지호 Lv.{level}",20,600,100,BLACK)
        if level<200:
            draw_text(screen,f"+{level+1}/클릭 {touch_money}/클릭",20,620,120,BLACK)
        else:
            draw_text(screen,f"+{level*2+2}/클릭 {touch_money}/클릭",20,620,120,BLACK)
        draw_text(screen,f"{cost}원",20,600,140,BLACK)
        draw_text(screen,f"동료구하기",40,620,240,BLACK)
        draw_text(screen,f"중요한물건",40,620,340,BLACK)
        draw_text(screen,f"환생하기",20,600,420,BLACK)
        if reincarnation_percent_calc()==False: 
            draw_text(screen,f"현재 불가능",20,600,440,BLACK)
        else:
            draw_text(screen,f"현재 {reincarnation_percent_calc()} % 추가",20,600,440,BLACK)
        if fever:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            draw_text(screen,f"피버타임 : {str(int(10 - elapsed_time))}초",30,150,30,(204,0,0))
        if type==1:
            if is_money==0:
                screen.blit(이미지,(300,80))
                draw_text(screen,"구걸실패...",30,200,120, BLACK)
            else:
                screen.blit(이미지4,(300,80))
                draw_text(screen,"히히돈이다",30,200, 120 ,BLACK)
        else:
            if fever:
                screen.blit(이미지5,(300,80))
            else:
                screen.blit(이미지1,(300,80))
            draw_text(screen,"돈주세요",30,200, 120 ,BLACK)
        draw_text(screen, f"현재 자금: {player_money}원", 30, screen.get_width() // 2, 50, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    x,y=pygame.mouse.get_pos()
                    if 500 <= x <= 750 and 80 <= y <= 160 and cost<=player_money:
                        player_money-=cost
                        level_up()
                    elif 500<=x<=750 and 200<=y<=280:
                        player_money=visit_convenience_store(player_money,screen)
                    elif 500<=x<=750 and 300<=y<=380:
                        player_money=trade_stocks(player_money,screen)
                    elif 500<=x<=750 and 400<=y<=480:
                        if reincarnation_percent_calc()!=0:
                            reincarnation()
                if random.randint(1,100)<=beg_probability:
                    player_money+=ceil(touch_money*plus_percent/100)
                    if fever:
                        player_money+=ceil(touch_money*plus_percent/100)
                    type=1
                    touch+=1
                    is_money=1
                else:
                    type=1
                    touch+=1
                    is_money=0
            if event.type == pygame.MOUSEBUTTONUP:
                type=0
        pygame.display.flip()
    return True

def visit_convenience_store(money, screen):
    global inventory,plus_percent
    team = [("심유묘 박주환",100000), ("코스프레남 이승민",300000), ("허수 최우혁",1000000), ("허리디스크 조준익",5000000), ("그냥 김민학",10000000), ("박경준",100000000), ("게임폐인 김인우",1000000000), 
             ("철학과 이준호",10000000000)]
    menu_option = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return money
            x,y=pygame.mouse.get_pos()
            if screen.get_width() // 2-400 <= x <= screen.get_width() // 2 +400:
                if 130<=y<=170:
                    menu_option = 0
                elif 180<=y<=220:
                    menu_option = 1
                elif 230<=y<=270:
                    menu_option = 2
                elif 280<=y<=320:
                    menu_option = 3
                elif 330<=y<=370:
                    menu_option = 4
                elif 380<=y<=420:
                    menu_option = 5
                elif 430<=y<=470:
                    menu_option = 6
                elif 480<=y<=520:
                    menu_option = 7
                elif 530<=y<=570:
                    menu_option = 8
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_option == len(team):
                    running = False
                    return money
                item, price = team[menu_option]
                price=ceil(price*(1.1**(inventory[item])))
                if money >= price and inventory[item]<40:
                    money -= price
                    inventory[item] += 1
                    plus_percent+=(menu_option+1)*2

        screen.fill(WHITE)
        for i, (item, price) in enumerate(team):
            pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-400,130 + i * 50,800,40],2)
            if inventory[item]==40:
                draw_text(screen, f"{item} - INF원 레벨:MAX", 30, screen.get_width() // 2, 150 + i * 50, BLACK if menu_option == i else (150, 150, 150))
            else:
                draw_text(screen, f"{item} - {ceil(price*(1.1**(inventory[item])))}원 레벨:{inventory[item]}", 30, screen.get_width() // 2, 150 + i * 50, BLACK if menu_option == i else (150, 150, 150))
        draw_text(screen, f"나가기", 30, screen.get_width() // 2,550, BLACK if menu_option==8 else (150, 150, 150))
        draw_text(screen, f"현재 자금: {money}원", 30, screen.get_width() // 2, 100, BLACK)
        pygame.display.flip()
    
    return money
# 주식 정보
stocks = {
    "김채원의 굿즈":{"price": 150000, "owned": 0}, 
    "알파카의 캡슐커피":{"price": 3000000, "owned": 0},
    "김종말의 다이어트 용품":{"price": 75000, "owned": 0},
    "한지호의 마블굿즈":{"price": 1500000, "owned": 0},
    "신희후의 노트북":{"price": 5000000, "owned": 0},
    "김수인의 코스프레 용품":{"price": 500000, "owned": 0}
}


def reincarnation_percent_calc():
    global percent
    percent=0
    if level<300:
        return 0
    percent+=1
    if level<400:
        percent+=2*(level-300)//5
    elif level<500:
        percent+=5*(level-400)//5+40
    elif level<600:
        percent+=20*(level-500)//5+140
    elif level<700:
        percent+=40*(level-600)//5+540
    elif level<800:
        percent+=60*(level-700)//5+1340
    elif level<900:
        percent+=80*(level-800)//5+2540
    elif level<1000:
        percent+=100*(level-900)//5+3540
    else:
        percent+=150*(level-1000)//5+4740
    return percent
    
# 주식 구매 및 판매
def trade_stocks(money, screen, action="buy"):
    global stocks,beg_probability
    menu_option = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return money
            
            x,y=pygame.mouse.get_pos()
            if screen.get_width() // 2-400 <= x <= screen.get_width() // 2 +400:
                if 130<=y<=170:
                    menu_option = 0
                elif 180<=y<=220:
                    menu_option = 1
                elif 230<=y<=270:
                    menu_option = 2
                elif 280<=y<=320:
                    menu_option = 3
                elif 330<=y<=370:
                    menu_option = 4
                elif 380<=y<=420:
                    menu_option = 5
                elif 430<=y<=470:
                    menu_option = 6
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_option == 6:
                    return money
                stock_name = list(stocks.keys())[menu_option]
                stock_price = stocks[stock_name]["price"]

                if action == "buy" and money >= stock_price and stocks[stock_name]["owned"]<10:
                    stocks[stock_name]["owned"] += 1
                    money -= stock_price
                    beg_probability +=1
                else:
                    draw_text(screen, "거래 실패", 30, screen.get_width() // 2, screen.get_height() // 2, BLACK)
                pygame.display.flip()
        screen.fill(WHITE)
        x,y=pygame.mouse.get_pos()
        for i, stock in enumerate(stocks.keys()):
            stock_info = stocks[stock]
            pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-400,130 + i * 50,800,40],2)
            draw_text(screen, f"{stock} - 가격: {stock_info['price']}원 / 보유량: {stock_info['owned']}", 30, screen.get_width() // 2, 150 + i * 50, BLACK if (screen.get_width() // 2-400<=x<=screen.get_width() // 2+400 and 130 + i * 50 <= y <=170 + i * 50) else (150, 150, 150))
        draw_text(screen, f"현재 자금: {money}원", 30, screen.get_width() // 2, 100, BLACK)
        pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-400,430,800,40],2)
        draw_text(screen, f"나가기", 30, screen.get_width() // 2, 450, BLACK if (screen.get_width() // 2-400<=x<=screen.get_width() // 2+400 and 430 <= y <= 470) else (150, 150, 150))
        pygame.display.flip()
    
    return money

def save_game():
    global beg_probability,plus_percent,level,cost,touch_money,player_money,inventory,reincarnate,reincarnate_plus_percent
    data = {'money': player_money, 'inventory': inventory, 'stocks': stocks,'level':level,'plus_percent':plus_percent,'beg_probability':beg_probability,'touch_money':touch_money,'cost':cost,'reincarnate':reincarnate,'reincarnate_plus_percent':reincarnate_plus_percent}
    with open(save_file, 'w') as f:
        json.dump(data, f)
    

def load_game():
    global inventory, player_money,cost,reincarnate_plus_percent,reincarnate
    global stocks, level, plus_percent,beg_probability,touch_money
    try:
        with open(save_file, 'r') as f:
            data = json.load(f)
        player_money = data['money']
        inventory = data['inventory']
        stocks = data['stocks']
        level = data['level']
        plus_percent = data['plus_percent']
        beg_probability = data['beg_probability']
        touch_money = data['touch_money']
        cost=data['cost']
        reincarnate_plus_percent=data['reincarnate_plus_percent']
        reincarnate=data['reincarnate']
        return True
    except FileNotFoundError:
        return False

#환생기능 구현 할거임 ㅋㅋ
def reincarnation():
    global player_money, inventory, cost, level, plus_percent, beg_probability, touch_money,stocks,reincarnate,reincarnate_plus_percent
    reincarnate+=1
    beg_probability=min(10+reincarnate,40)
    player_money = 0
    reincarnate_plus_percent+=1
    if level<400:
        reincarnate_plus_percent+=2*(level-300)//5
    elif level<500:
        reincarnate_plus_percent+=5*(level-400)//5+40
    elif level<600:
        reincarnate_plus_percent+=20*(level-500)//5+140
    elif level<700:
        reincarnate_plus_percent+=40*(level-600)//5+540
    elif level<800:
        reincarnate_plus_percent+=60*(level-700)//5+1340
    elif level<900:
        reincarnate_plus_percent+=80*(level-800)//5+2540
    elif level<1000:
        reincarnate_plus_percent+=100*(level-900)//5+3540
    else:
        reincarnate_plus_percent+=150*(level-1000)//5+4740
    plus_percent=100+reincarnate_plus_percent
    level=1
    cost=10
    touch_money=1
    inventory = {"김채원의 굿즈":0, "알파카의 캡슐커피":0, "김종말의 다이어트 용품":0, "한지호의 마블굿즈":0,"신희후의 노트북":0,"김수인의 코스프레 용품":0,
             "심유묘 박주환":0, "코스프레남 이승민":0, "허수 최우혁":0, "허리디스크 조준익":0, "그냥 김민학":0, "박경준":0, "게임폐인 김인우":0, "철학과 이준호":0}
    stocks = {
    "김채원의 굿즈":{"price": 150000, "owned": 0}, 
    "알파카의 캡슐커피":{"price": 3000000, "owned": 0},
    "김종말의 다이어트 용품":{"price": 75000, "owned": 0},
    "한지호의 마블굿즈":{"price": 1500000, "owned": 0},
    "신희후의 노트북":{"price": 5000000, "owned": 0},
    "김수인의 코스프레 용품":{"price": 10000000, "owned": 0}
    }
