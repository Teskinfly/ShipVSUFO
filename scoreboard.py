import pygame.font
class Scoreboard():
    def __init__(self, ai_settings, screen, stats):###分数板初始化
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_level()
    def prep_score(self):###分数显示的模型，位置初始化
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color,
        self.ai_settings.bg_color)
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    def show_score(self):###显示分数
        self.screen.blit(self.score_image, self.score_rect)
    def prep_level(self):###关卡显示模型，位置初始化
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.text_color,self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.top
        self.level_rect.centerx = self.screen_rect.centerx
    def show_level(self):###显示关卡
        self.screen.blit(self.level_image,self.level_rect)
        
