import pygame
class Ship():

    def __init__(self,ai_settings,screen):###初始化
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx ###中心x与屏幕中心x一致
        self.rect.bottom = self.screen_rect.bottom ### 底下与屏幕底下一致
        ### 移动状态
        self.moving_right = False 
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        ### 飞船坐标
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
    def blitme(self):
        ###重绘
        self.screen.blit(self.image,self.rect)
    def update(self): ###坐标范围的判定，不能让飞船跳到外面去
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        elif self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.centery = self.centery
    def center_ship(self): ###让飞船回到初始之地
        self.center = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom - 1/2*(self.rect.bottom-self.rect.top)
