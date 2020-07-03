import pygame.font
class Button():
    def __init__(self,ai_settings,screen,msg):###开始按钮初始化
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width,self.height = 200,50
        self.button_color = (66,66,66)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        self.pre_msg(msg)
    def pre_msg(self,msg): ###输入内容
        self.msg_img = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center
    def draw_button(self):###绘制
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_img,self.msg_img_rect)
    
