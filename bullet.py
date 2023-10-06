import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from ship"""
    
    def __init__(self, ss_game):
        """Create bullet object at ship's current position"""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.color = self.settings.bullet_color
        
        # Create bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
                                self.settings.bullet_height)
        self.rect.midright = ss_game.ship.rect.midright
        
        # Store bullet's position as float
        self.x = float(self.rect.x)
        
        
    def update(self):
        """Move bullet across screen"""
        # update exact position of bullet
        self.x += self.settings.bullet_speed
        # update rect position
        self.rect.x = self.x
        
        
    def draw_bullet(self):
        """Draw bullet to screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)