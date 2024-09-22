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

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller로 패키징된 실행 파일인 경우
        return os.path.dirname(sys.executable)
    else:
        # 개발 환경에서 실행하는 경우
        return os.path.dirname(os.path.abspath(__file__))

def get_save_file_path():
    executable_path = get_executable_path()
    return os.path.join(executable_path, 'save_file.json')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
button_color = pygame.Color("#FFEECF")
player_money = 21
touch_money = 1
plus_percent = 100
level=1
cost=10
reincarnate=0
reincarnate_coins=0
auto_touch=0
inventory = {"김채원의 굿즈":0, "알파카의 캡슐커피":0, "김종말의 다이어트 용품":0, "한지호의 마블굿즈":0,"신희후의 노트북":0,"김수인의 코스프레 용품":0,
             "심유묘 박주환":0, "코스프레남 이승민":0, "허수 최우혁":0, "허리디스크 조준익":0, "그냥 김민학":0, "박경준":0, "게임폐인 김인우":0, "철학과 이준호":0,
             "피버 배율 증가":0, "자동 터치":0, "시작 레벨 증가":0,"엔딩 보기":0}
save_file = get_save_file_path()
beg_probability=10
reincarnate_plus_percent=0

def find_coin():
    reincarnate_coins=0
    reincarnate_coins+=inventory["심유묘 박주환"]
    reincarnate_coins+=inventory["코스프레남 이승민"]
    reincarnate_coins+=inventory["허수 최우혁"]
    reincarnate_coins+=inventory["허리디스크 조준익"]
    reincarnate_coins+=inventory["그냥 김민학"]
    reincarnate_coins+=inventory["박경준"]
    reincarnate_coins+=inventory["게임폐인 김인우"]
    reincarnate_coins+=inventory["철학과 이준호"]
    return reincarnate_coins

def reincarnate_level_up():
    global level,touch_money
    starting_level=inventory["시작 레벨 증가"]
    level+=starting_level
    if starting_level>=200:
        touch_money+=(starting_level-200)*(starting_level-199)//2
    touch_money+=(starting_level)*(starting_level+1)//2
def level_up():
    global level
    global cost
    global touch_money
    level+=1
    if level>200:
        touch_money+=level
    touch_money+=level
    if level<=200:
        cost*=1.05
    elif level<=300:
        cost*=1.04
    else:
        cost*=1.03
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
    page=1
    start_ticks = pygame.time.get_ticks()
    auto_tick=pygame.time.get_ticks()
    while running:
        save_game()
        if fever==0 and touch>=50:
            fever=1
            touch=0
            start_ticks = pygame.time.get_ticks()
        if fever==1:
            if (pygame.time.get_ticks()-auto_tick)>=500:
                auto_tick=pygame.time.get_ticks()
                player_money+=inventory["자동 터치"]*(ceil(touch_money*plus_percent/100)*(1+inventory["피버 배율 증가"]))
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            if elapsed_time>=10:
                fever=0
            touch=0
        else:
            if (pygame.time.get_ticks()-auto_tick)>=500:
                auto_tick=pygame.time.get_ticks()
                player_money+=inventory["자동 터치"]*(ceil(touch_money*plus_percent/100))
        screen.fill(WHITE)
        pygame.draw.rect(screen, button_color, pygame.Rect(100, 400, 200, 100), border_radius=20)
        draw_text(screen,f"환생상점",40,200,440, BLACK)
        pygame.draw.rect(screen,button_color, pygame.Rect(500, 80, 250, 80), border_radius=20)
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
        if page==1:
            draw_text(screen,f"동료구하기",40,620,240,BLACK)
            draw_text(screen,f"중요한물건",40,620,340,BLACK)
            draw_text(screen,f"환생하기",20,600,420,BLACK)
            if reincarnation_percent_calc()==False: 
                draw_text(screen,f"현재 불가능",20,600,440,BLACK)
            else:
                draw_text(screen,f"현재 {reincarnation_percent_calc()} % 추가",20,600,440,BLACK)
                draw_text(screen,f"환생코인 {find_coin()} 획득",20,600,460,BLACK)
                
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
                elif 100<=x<=300 and 400<=y<=500:
                    reincarnate_shop(screen)
                if random.randint(1,100)<=beg_probability:
                    player_money+=ceil(touch_money*plus_percent/100)
                    if fever:
                        player_money+=(ceil(touch_money*plus_percent/100)*(1+inventory["피버 배율 증가"]))
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


def reincarnate_shop(screen):
    global inventory,plus_percent,reincarnate_coins
    team = [("피버 배율 증가",10), ("자동 터치",10), ("시작 레벨 증가",10), ("엔딩 보기",2147483647)]
    menu_option = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return reincarnate_coins
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_option == len(team):
                    running = False
                    return reincarnate_coins
                item, price = team[menu_option]
                price+=inventory[item]
                if reincarnate_coins >= price and inventory[item]<2147483648:
                    reincarnate_coins -= price
                    inventory[item] += 1

        screen.fill(WHITE)
        draw_text(screen, f"피버 배율 증가- { 10+inventory['피버 배율 증가']}원 현재: {1+inventory['피버 배율 증가'] }배", 30, screen.get_width() // 2, 150, BLACK if menu_option == 0 else (150, 150, 150))
        draw_text(screen, f"자동 터치- { 10+inventory['자동 터치']}원  현재: 0.5초당 {inventory['자동 터치']}번", 30, screen.get_width() // 2, 200, BLACK if menu_option == 1 else (150, 150, 150))
        draw_text(screen, f"시작 레벨 증가- { 10+inventory['시작 레벨 증가']}원 현재 시작 레벨:{inventory['시작 레벨 증가']}", 30, screen.get_width() // 2, 250, BLACK if menu_option == 2 else (150, 150, 150))
        draw_text(screen, "엔딩보기- 2147483647 코인", 30, screen.get_width() // 2, 300, BLACK if menu_option == 3 else (150, 150, 150))
        for i, (item, price) in enumerate(team):
            pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-400,130 + i * 50,800,40],2)
        pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-400,330,800,40],2)
        draw_text(screen, f"나가기", 30, screen.get_width() // 2,350, BLACK if menu_option==4 else (150, 150, 150))
        draw_text(screen, f"현재 환생 코인: {reincarnate_coins}원", 30, screen.get_width() // 2, 100, BLACK)
        pygame.display.flip()
    
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
                price=ceil(price*(1.02**(inventory[item])))
                if money >= price and inventory[item]<2147483648:
                    money -= price
                    inventory[item] += 1
                    plus_percent+=(menu_option+1)*5

        screen.fill(WHITE)
        for i, (item, price) in enumerate(team):
            pygame.draw.rect(screen,BLACK,[screen.get_width() // 2-400,130 + i * 50,800,40],2)
            if inventory[item]==2147483648:
                draw_text(screen, f"{item} - INF원 레벨:MAX", 30, screen.get_width() // 2, 150 + i * 50, BLACK if menu_option == i else (150, 150, 150))
            else:
                draw_text(screen, f"{item} - {ceil(price*(1.02**(inventory[item])))}원 레벨:{inventory[item]}", 30, screen.get_width() // 2, 150 + i * 50, BLACK if menu_option == i else (150, 150, 150))
        draw_text(screen, f"나가기", 30, screen.get_width() // 2,550, BLACK if menu_option==8 else (150, 150, 150))
        draw_text(screen, f"현재 자금: {money}원", 30, screen.get_width() // 2, 100, BLACK)
        pygame.display.flip()
    
    return money
# 주식 정보
stocks = {
    "김채원의 굿즈":{"price": 100000, "owned": 0}, 
    "알파카의 캡슐커피":{"price": 40000, "owned": 0},
    "김종말의 다이어트 용품":{"price": 75000, "owned": 0},
    "한지호의 마블굿즈":{"price": 300000, "owned": 0},
    "신희후의 노트북":{"price": 500000, "owned": 0},
    "김수인의 코스프레 용품":{"price": 1000000, "owned": 0}
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
    percent*=10
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
    global beg_probability,plus_percent,level,cost,touch_money,player_money,inventory,reincarnate,reincarnate_plus_percent,reincarnate_coins
    data = {'money': player_money, 'inventory': inventory, 'stocks': stocks,'level':level,'plus_percent':plus_percent,'beg_probability':beg_probability,'touch_money':touch_money,'cost':cost,'reincarnate':reincarnate,'reincarnate_plus_percent':reincarnate_plus_percent,'reincarnate_coins':reincarnate_coins}
    with open(save_file, 'w') as f:
        json.dump(data, f)
    

def load_game():
    global inventory, player_money,cost,reincarnate_plus_percent,reincarnate
    global stocks, level, plus_percent,beg_probability,touch_money,reincarnate_coins
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
        reincarnate_coins=data['reincarnate_coins']
        return True
    except FileNotFoundError:
        return False

#환생기능 구현 할거임 ㅋㅋ
def reincarnation():
    global player_money, inventory, cost, level, plus_percent, beg_probability, touch_money,stocks,reincarnate,reincarnate_plus_percent,reincarnate_coins
    reincarnate+=1
    beg_probability=min(10+reincarnate,40)
    player_money = 21
    reincarnate_plus_percent+=reincarnation_percent_calc()
    plus_percent=100+reincarnate_plus_percent
    level=1
    cost=10
    touch_money=1
    reincarnate_coins+=find_coin()
    피버_배율_증가=inventory["피버 배율 증가"]
    자동_터치=inventory["자동 터치"]
    시작_레벨_증가=inventory["시작 레벨 증가"]
    엔딩_보기=inventory["엔딩 보기"]
    inventory = {"김채원의 굿즈":0, "알파카의 캡슐커피":0, "김종말의 다이어트 용품":0, "한지호의 마블굿즈":0,"신희후의 노트북":0,"김수인의 코스프레 용품":0,
             "심유묘 박주환":0, "코스프레남 이승민":0, "허수 최우혁":0, "허리디스크 조준익":0, "그냥 김민학":0, "박경준":0, "게임폐인 김인우":0, "철학과 이준호":0,
             "피버 배율 증가":피버_배율_증가, "자동 터치":자동_터치, "시작 레벨 증가":시작_레벨_증가,"엔딩 보기":엔딩_보기}
    stocks = {
    "김채원의 굿즈":{"price": 100000, "owned": 0}, 
    "알파카의 캡슐커피":{"price": 40000, "owned": 0},
    "김종말의 다이어트 용품":{"price": 75000, "owned": 0},
    "한지호의 마블굿즈":{"price": 300000, "owned": 0},
    "신희후의 노트북":{"price": 500000, "owned": 0},
    "김수인의 코스프레 용품":{"price": 1000000, "owned": 0}
    }
    reincarnate_level_up()
