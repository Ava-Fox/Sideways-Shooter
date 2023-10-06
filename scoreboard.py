import pygame.font
import pygame.transform
from pygame.sprite import Group

from pathlib import Path
import json

from sushi import Sushi

class Scoreboard:
    """A class to report scoring info"""
    
    def __init__(self, ss_game):
        """Initialzie scorekeeping attributes"""
        self.ss_game = ss_game
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ss_game.settings
        self.stats = ss_game.stats
        
        # Font settings for scoring info
        self.text_color = (251, 245, 253)
        self.font = pygame.font.SysFont(None, 48)
        
        # Prepare initial score image
        self.prep_score()
        self.prep_ultimate_high_score()
        self.prep_high_score()
        self.prep_ships()
        
        
    def prep_score(self):
        """Turn score into rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, 
                                            self.settings.bg_color)
        self.score_image = pygame.transform.rotate(self.score_image, -90)
        
        
        # Display score at bottom right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.bottom = self.screen_rect.bottom - 20
        
    def show_score(self):
        """Draw score to screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)
        
    def prep_high_score(self):
        """Turn high score into rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, 
                                                 self.text_color, 
                                                 self.settings.bg_color)
        self.high_score_image = pygame.transform.rotate(
            self.high_score_image, -90)
        
        
        # Center high score at mid right of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.centery = self.screen_rect.centery
        
    def check_high_score(self):
        """Check to see if there's new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            
    def prep_ships(self):
        """Show how many ships left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Sushi(self.ss_game)
            ship.rect.right = self.screen_rect.right - 20
            ship.rect.top = 20 + ship_number * ship.rect.height
            self.ships.add(ship)
            
    def prep_ultimate_high_score(self):
        """Search for existing json file that holds ultimate high score info"""
        path = Path('all-time_high_score.json')
        if path.exists():
            contents = path.read_text()
            ult_high_score = json.loads(contents)
            self.stats.high_score = ult_high_score
        else:
            return None
        
    def save_ultimate_high_score(self):
        """
        Check if high score is larger than one loaded on json file and replace it
        """
        path = Path('all-time_high_score.json')
        ult_high_score = path.read_text()
        if int(ult_high_score) < self.stats.high_score:
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)
            
            
# Ok, trying to save the ultimate high score, and thinking about doing so effectively.
    # have a prep_ultimate_high_score method here, where searches for existing json file that holds info
    # Compares existing u high score to current high score and if they have a larger one currently it rewrites the json file