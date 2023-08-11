import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''A class to represent a single alien in the fleet.'''

    def __init__(self, ai_game):
        '''Initialize the alien and set its starting position.'''
        super().__init__() # inherit sprite 
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top of the screen.
        # self.rect.x 和y 分别代表外星人图片左上角在游戏屏幕里的坐标，这段代码为了让外星人出现时稍稍偏移顶端，这样不会顶格出现
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien’s exact horizontal position.
        self.x = float(self.rect.x)
