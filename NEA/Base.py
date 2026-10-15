'''
this is going to be the basic class for all objects that need to be drawn in my game
all objects are going to need a pos vector and a type
'''

import pygame

class Base:
    def __init__(self, pos, type, client):
        self.pos = pygame.Vector2(pos)
        self.type = type
        client.mainList.append(self)