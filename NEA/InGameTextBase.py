'''

this is going to be the main base class for all items that need to be displayed when the game is running

'''
import pygame

from Base import Base

class InGameTextBase(Base):
    def __init__(self, client):
        super().__init__((10,10), 'TD', client)
        self.font = pygame.font.SysFont('Arial', 11)
        self.text = ''