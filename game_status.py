class GameStatus():
    def __init__(self, ai_settings):###游戏状态初始化
        self.ai_settings = ai_settings
        self.reset_status()
        self.game_active = False
    def reset_status(self):###重置游戏后，分数与关卡清零
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
