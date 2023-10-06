import pygame
from pygame.sprite import Sprite

class Sushi(Sprite):
    """a class to manage sushi ship"""
    
    def __init__(self, ss_game):
        """Initialize ship and set its starting position"""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.screen_rect = ss_game.screen.get_rect()
        
        # Load ship image and get its rect
        self.image = pygame.image.load('images/sushi.png')
        self.rect = self.image.get_rect()
        
        # Start each new ship at mid left of screen
        self.rect.midleft = self.screen_rect.midleft
        
        # Store float for ship's exact vertical position
        self.y = float(self.rect.y)
        
        # Movement flag; start w a ship that's not moving
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
        """Update ship's position based on movement flag"""
        # Update ship's y value, not rect   
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        #Update rect object from self.y
        self.rect.y = self.y    
        
    def blitme(self):
        """Draw ship at its current location"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Center ship midleft of screen"""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)