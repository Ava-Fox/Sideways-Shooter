import pygame

class Music:
    """ a class to hold music settings"""
    
    def __init__(self, ss_game):
        """Initialize music"""
        pygame.mixer.music.load('music/cute_lil_diddy.wav')
        pygame.mixer.music.play()
        pygame.mixer.music.queue('music/ss_background.wav')
       
        
    def bullet_sound(self):
        """play bullet sound"""
        bullet_sound = pygame.mixer.Sound("music/bullet_sound.wav")
        pygame.mixer.Sound.play(bullet_sound)
        
    def explosion(self):
        """play explosion sound"""
        explosion_sound = pygame.mixer.Sound("music/explosion.wav")
        pygame.mixer.Sound.play(explosion_sound)
       