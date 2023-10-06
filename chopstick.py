import pygame
from pygame.sprite import Sprite

class Chopstick(Sprite):
    """A class to represent a single chopstick in fleet"""
    
    def __init__(self, ss_game):
        """Initialize chopstick and set its starting position"""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        
        # Load image and set its rect attribute
        self.image = pygame.image.load('images/chopsticks.png')
        self.rect = self.image.get_rect()
        
        # Start each new chopstick newr far right of screen
        self.rect.x = (self.screen.get_rect().right - 2 * self.rect.width)
        self.rect.y = self.rect.height
        
        # Store chopstick's exact vertical position
        self.y = float(self.rect.y)
        
    def check_edges(self):
        """Return True if chopstick at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.top <= 0) or (self.rect.bottom >= screen_rect.bottom)
    
    def update(self):
        """Move alien up or down"""
        self.rect.y += self.settings.chopstick_speed * self.settings.fleet_direction  