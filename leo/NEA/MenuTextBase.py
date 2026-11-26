'''

this is going to be the main base class for all items that need to be displayed when the game is running

'''
import pygame

from Base import Base

class MenuTextBase(Base):
    def __init__(self, client, pos):

        #passing up the main information and creating the extra needed variables
        super().__init__(pos, 'TDM', client)
        self.font = pygame.font.SysFont('Arial', 11)
        self.text = ''