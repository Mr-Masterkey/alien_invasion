import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''Overall class to manage game assets and behacior.'''
    def __init__(self):
        '''initialize the game, and create game resources.'''
        pygame.init()
        self.settings = Settings()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #set fullscreen
        '''
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        '''
        pygame.display.set_caption('Alien Invasion')

        #Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self._create_fleet()

    def run_game(self):
        '''Start the main loop dor the game.'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()          

    def _check_events(self):    
        # respond to keyboard and mouse events.           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    
    def _check_keydown_events(self, event):
        '''Respond to keypresses.'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q: # you should use english keyboard input to press the letter key
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _check_keyup_events(self,event):
        '''respond to key releases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                        
    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group.'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        "update position of bullets and get rid of  old bullets"
        self.bullets.update()
        
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy(): # we don't want to remove bullet during loop,so we build a copy and remove copy
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''respond to bullet-alien collisions.'''
        # check for any bullets that have hit aliens
        # if so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens, True, True) # two true ask pygame delete  both bullet and alien
        if not self.aliens:
            #destroying existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()


    def _update_screen(self):
        '''updaye images on the screen, and flip to the new screen'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)          

        #Make the most recently drawn screen visible.
        pygame.display.flip()

    def _create_fleet(self):
        '''Create the fleet of aliens.'''
        # create an alien and find the number of aliens in a row
        #Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #determine the number of row os aliens that fit on the screen
        ship_height  = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height # subtacting 1 alien from the top, 2 aliens + ship from the bottom
        number_rows = available_space_y // (2 * alien_height)

        # Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
        #Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        '''Update the positions of all aliens in the fleet.'''
        '''check if the fleet is at an edge, then update the position of alll aliens in the fleet.'''
        self._check_fleet_edge()
        self.aliens.update()

        #Look for alien_ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edge(self):
        '''Respond appropriately if any aliens have reached an esge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction.'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        '''Respond to the ship being hit by an alien.'''
        # Decrement ship_left.
        self.stats.ships_left -= -1

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        #pause.
        sleep(0.5)

    def _check_aliens_bottom(self):
        '''check if any aliens have reached the bottom of the screen.'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got hit.
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make a game intance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

        