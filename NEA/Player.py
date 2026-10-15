'''
this is going to be the main class for the player object. It is going to need to use the Base class as its parent class
'''
import pygame

#importing the main basic class for all objects that need to be rendered including the player
from Base import Base

class Player(Base):
    def __init__(self, client):
        # passing the players type as a ellipsis
        super().__init__((0,0), 'E', client)

        #then creating this objects rect so it can be drawn
        self.rect = pygame.Rect(self.pos.x - 7.5, self.pos.y - 7.5, 15, 15)

        #this motion vector will make it so the players bounce around a bit move and slide like real balls on a flat plane
        self.motion = pygame.Vector2(0, 0)

    def move(self, speed):
        #here i am doing the logic for when the player presses a key and makes it so the players motion vec gets modified so the player can move
        keys = pygame.key.get_pressed()

        #setting up the vector that modifies the motion
        move_vector = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            move_vector.y -= speed
        if keys[pygame.K_s]:
            move_vector.y += speed
        if keys[pygame.K_a]:
            move_vector.x -= speed
        if keys[pygame.K_d]:
            move_vector.x += speed

        #applying the made vector to the motion
        self.motion += move_vector

