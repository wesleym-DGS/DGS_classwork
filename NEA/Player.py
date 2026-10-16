'''
this is going to be the main class for the player object. It is going to need to use the Base class as its parent class
'''
import pygame

#importing the main basic class for all objects that need to be rendered including the player
from Base import Base

class Player(Base):
    def __init__(self, client):

        # passing the players type as a ellipsis
        super().__init__((100,100), 'E', client)

        #then creating this objects rect so it can be drawn
        self.rect = pygame.Rect(self.pos.x - 7.5, self.pos.y - 7.5, 15, 15)

        #this motion vector will make it so the players bounce around a bit move and slide like real balls on a flat plane
        self.motion = pygame.Vector2(0, 0)

    def move(self, speed, dt):

        #here i am doing the logic for when the player presses a key and makes it so the players motion vec gets modified so the player can move
        keys = pygame.key.get_pressed()

        #setting up the vector that modifies the motion
        move_vector = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            move_vector.y -= speed * dt
        if keys[pygame.K_s]:
            move_vector.y += speed * dt
        if keys[pygame.K_a]:
            move_vector.x -= speed * dt
        if keys[pygame.K_d]:
            move_vector.x += speed * dt

        #trying to normalize the movement vector but catching the error if it is zero
        try:

            #normalizing the move vector so that diagonal movement doesn't cause extra movement
            move_vector.normalize()

        except ValueError:

            #if the error happens then we just move on
            pass

        #applying the made vector to the motion
        self.motion += move_vector

    def check_bounds(self, bounce):

        #checking to see if the player is outside the bounds of the game and if they are,
        #inverting there momentum so  they get back into the bounds of the game
        if self.pos.x < 0 or self.pos.x > 785:
            self.motion.x = -self.motion.x * bounce
        if self.pos.y < 0 or self.pos.y > 585:
            self.motion.y = -self.motion.y * bounce

    def update(self, renderList, dt):

        #when the game updates this object the player needs move
        self.move(50, dt)

        #applying the motion that was gathered in the move method
        self.pos += self.motion

        #slowing the player down to mimic air resistance
        self.motion += (-self.motion) * 0.05

        #executing the bounds check and making it so they get put back into the screen
        self.check_bounds(1)

        #this is when the rect for the player rendering gets updated to the current pos
        self.rect = pygame.Rect(self.pos.x - 7.5, self.pos.y - 7.5, 15, 15)

        #adding the object to the freshly flushed render list
        renderList.append([self.type, (255,0,0), self.rect])

        #this was a debug line to see if the players pos was working
        #print(self.pos)