import sys
import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
import game_functions as gf
from alien import Alien
from game_status import GameStatus
from button import Button
from scoreboard import Scoreboard
def run_game():
        pygame.init() ###初始化
        ai_settings = Settings() ###设置类
        screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))  ###屏幕显示
        ship = Ship(ai_settings,screen) ###飞船
        pygame.display.set_caption("飞船大战UFO") ###标题
        play_button = Button(ai_settings,screen,"Start Game") ###开始按钮
        bullets = Group() ###子弹组
        aliens = Group() ###外星人组
        gf.create_fleet(ai_settings,ship,screen,aliens) ##创建外星人舰队
        status = GameStatus(ai_settings) ###游戏状态
        sb = Scoreboard(ai_settings,screen,status) ###分数板显示分数与关卡
        while True:
                gf.check_events(ai_settings,screen,ship,bullets,status,play_button,aliens)###事件监听
                if status.game_active:  ###若是游戏中
                        ship.update() ###飞船状态更新
                        gf.update_bullet(ai_settings,ship,screen,aliens,bullets,sb,status)### 子弹状态更新
                        gf.update_aliens(ai_settings,status,screen,ship,aliens,bullets)### 外星人更新
                gf.update_screen(ai_settings,screen,ship,bullets,aliens,play_button,status,sb) ###屏幕更新重绘
                
run_game()
