import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from sushi import Sushi
from bullet import Bullet
from chopstick import Chopstick
from music import Music
from button import Button
from scoreboard import Scoreboard


class SidewaysShooter:
    """Overall class to manage game assets and behavior"""
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
       # self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Sideways Shooter")
        
        
        # Create an instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Sushi(self)
        self.bullets = pygame.sprite.Group()
        self.chopsticks = pygame.sprite.Group()
        self.music = Music(self)
        
        self._create_fleet()
        
        #Start game in inactive state
        self.game_active = False
        
        # Make Play button
        self.play_button = Button(self, "Play!")
    def run_game(self):
        """Start main loop for game"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_chopsticks()
                self.sb.save_ultimate_high_score()
                
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
               
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                    
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)    
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    
    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _check_keyup_events(self, event):
        """Respond to key release"""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
            
    
    def _check_play_button(self, mouse_pos):
        """Start new game when player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_ships()
            self.game_active = True
            
            # Get rid of any remaining bullets/aliens
            self.bullets.empty()
            self.chopsticks.empty()
            
            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            
            # Hide mouse cursor
            pygame.mouse.set_visible(False)
    def _fire_bullet(self):
        """Create a new bullet and add it to bullet's group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.music.bullet_sound()
            
    def _create_fleet(self):
        """Create the fleet of chopsticks"""
        chopstick = Chopstick(self)
        chopstick_width, chopstick_height = chopstick.rect.size
        
        current_x, current_y = chopstick.rect.x, chopstick_height
        
        while current_y < (self.settings.screen_height - chopstick_height):
            while current_x > (self.settings.screen_width // 2):
                self._create_chopstick(current_x, current_y)
                current_x -= 2 * chopstick_width
                
            #Finished a row; reset x value, and increment y value
            current_x = chopstick.rect.x 
            current_y += 2 * chopstick_height
                
    def _create_chopstick(self, x_position, y_position):
        """Create chopstick"""
        new_chopstick = Chopstick(self)
        new_chopstick.rect.x = x_position
        new_chopstick.rect.y = y_position
        self.chopsticks.add(new_chopstick)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet positions
        self.bullets.update()
        
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
                
        self._check_bullet_chopstick_collisions()
        
    def _check_bullet_chopstick_collisions(self):
        """Respond to bullet/chopstick collisions"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.chopsticks, True, True)
        if collisions:
            self.music.explosion()
            for chopsticks in collisions.values():
                self.stats.score += self.settings.chopstick_points * len(chopsticks)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.chopsticks:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
        
    def _check_chopsticks_side(self):
        """Check if any chopsticks reached side of fleet"""
        for chopstick in self.chopsticks.sprites():
            if chopstick.rect.left <= 0:
                self._ship_hit()
                break
                
    def _update_chopsticks(self):
        """Update positions of all chopsticks in fleet"""
        self._check_fleet_edges()
        self.chopsticks.update()
        
        if pygame.sprite.spritecollideany(self.ship, self.chopsticks):
            self._ship_hit()
            
        self._check_chopsticks_side()
        
    def _ship_hit(self):
        """Respond to ship being hit by chopstick"""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining chopsticks and bullets
            self.bullets.empty()
            self.chopsticks.empty()

            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            self.music.explosion()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
        
    def _check_fleet_edges(self):
        """Respond appropriately if any chopsticks have reached an edge"""
        for chopstick in self.chopsticks.sprites():
            if chopstick.check_edges():
                self._change_fleet_direction()
                break
                
    def _change_fleet_direction(self):
        """Drop the entire fleet and change direction"""
        for chopstick in self.chopsticks.sprites():
            chopstick.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_screen(self):
        """Update images on screen and flip to new screen"""
        # Redraw screen during each pass thru loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.chopsticks.draw(self.screen)
        
        # Draw score info
        self.sb.show_score()
        
        # Draw play button if game inactive
        if not self.game_active:
            self.play_button.draw_button()
        
        #Make most recently drawn screen visible
        pygame.display.flip()
            
if __name__ == '__main__':
    # Make a game instance, and run game
    ss = SidewaysShooter()
    ss.run_game()