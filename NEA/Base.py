'''
this is going to be the basic class for all objects that need to be drawn in my game
all objects are going to need a pos vector and a type
'''

import pygame

class Base:
    def __init__(self, pos, type, client):

        #all objects need to have a pos vector so they can be drawn on the screen
        self.pos = pygame.Vector2(pos)

        #they also need to have a type so they can be drawn by the rendering pipline
        self.type = type

        #and all objects need to be added to the main list so the game will update them
        client.mainList.append(self)