import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    '''Overall class to manage game assets and behacior.'''
    def __init__(self):
        '''initialize the game, and create game resources.'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_with, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)

    def run_game(self):
        '''Start the main loop dor the game.'''
        while True:
            self._check_events()
            self._upgrade_screen()          

    def _check_events(self):
        # respond to keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def _upgrade_screen(self):
        '''updaye images on the screen, and flip to the new screen'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()              

        #Make the most recently drawn screen visible.
        pygame.display.flip()
if __name__ == '__main__':
    # Make a game intance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

        