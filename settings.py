class Settings:
    """"A settings class to store all settings"""
    
    def __init__(self):
        """Initialize game's static settings"""
        # screen settings
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (250, 121, 213)
        
        # Ship settings
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_speed = 12.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (121, 217, 250)
        self.bullets_allowed = 3
        
        # Chopstick settings
        self.fleet_drop_speed = 100
        
        # How quickly game speeds up
        self.speedup_scale = 1.1
        # How quickly alien point values increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout game"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.chopstick_speed = 1.0
        
        self.fleet_direction = 1
        
        # Scoring settings
        self.chopstick_points = 50
        
    def increase_speed(self):
        """Increase speed and alien point values settings"""
        self.ship_speed *= self.speedup_scale
        self.chopstick_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        
        #use int to increase point val by whole integers:
        self.chopstick_points = int(self.chopstick_points * self.score_scale) 