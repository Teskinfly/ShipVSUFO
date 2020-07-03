import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
def check_keydown_events(event,ai_settings,screen,ship,bullets):###监测按钮按下
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
    elif event.key == pygame.K_z:
        sys.exit()
    elif event.key == pygame.K_q:
        ai_settings.bullet_width = 1000
    elif event.key == pygame.K_w:
        ai_settings.alien_speed_factor = 1
    elif event.key == pygame.K_e:
        ai_settings.alien_points = 500
def check_keyup_events(event,ai_settings,screen,ship,bullets):###监测按钮松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False    
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
def check_events(ai_settings,screen,ship,bullets,status,play_button,aliens):###监听各种事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(status,play_button,mouse_x,mouse_y,aliens,bullets,ship,ai_settings,screen)
def check_play_button(status,play_button,mouse_x,mouse_y,aliens,bullets,ship,ai_settings,screen):###监听开始按键
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not status.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        status.reset_status()
        status.game_active = True
        status.level = 1
        status.score = 0
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,ship,screen,aliens)
        ship.center_ship()   
def update_screen(ai_settings,screen,ship,bullets,aliens,play_button,status,sb):###屏幕的一切重绘，保证动态性
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    sb.show_score()
    sb.show_level()
    aliens.draw(screen)
    if not status.game_active:
        play_button.draw_button()
    pygame.display.flip() ###重绘显示
def update_bullet(ai_settings,ship,screen,aliens,bullets,sb,status): ###
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:###子弹到头了，就删掉
                bullets.remove(bullet)
        check_bullet_alien_collisions(ai_settings,ship,screen,aliens,bullets,sb,status)
def check_bullet_alien_collisions(ai_settings,ship,screen,aliens,bullets,sb,status):###监听子弹与UFO碰撞
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:###发生碰撞，一起消失
        for aliens in collisions.values():                
            status.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
    if len(aliens)==0:###外星人为空，就重置游戏，并升级难度
        bullets.empty()
        ai_settings.increase_speed()
        status.level += 1
        sb.prep_level()
        create_fleet(ai_settings,ship,screen,aliens)
def get_number_aliens_x(ai_settings,alien_width):###根据屏幕计算外星人数量
    available_space_x = ai_settings.screen_width-2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
def create_alien(ai_settings,screen,aliens,alien_number,row_number):###创建外星人，初始化参数，并添加至舰队
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)
def create_fleet(ai_settings,ship,screen,aliens):###创建舰队
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)
def update_aliens(ai_settings,status,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,status,screen,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,status,screen,ship,aliens,bullets)
def get_number_rows(ai_settings,ship_height,alien_height):###计算出外星人有多少行
    available_space_y = (ai_settings.screen_height -(3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():###监测舰队是否移动到屏幕的边境
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):###改变舰队方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def ship_hit(ai_settings,status,screen,ship,aliens,bullets):###飞船被撞击后
    if status.ships_left > 1:###生命还有
        status.ships_left -= 1
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,ship,screen,aliens)
        ship.center_ship()
        sleep(0.5)
    else: ###没有生命了
        status.game_active = False 
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings,status,screen,ship,aliens,bullets): ##监听外星UFO是否突破防线
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:###到达底部
            ship_hit(ai_settings,status,screen,ship,aliens,bullets)
            break


