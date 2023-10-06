class GameStats:
    """Track statistics for Sideways Shooter"""
    
    def __init__(self, ss_game):
        """Initialize statistics"""
        self.settings = ss_game.settings
        self.reset_stats()
        self.high_score = 0
        
    def reset_stats(self):
        """Initialize stats that can change during game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0