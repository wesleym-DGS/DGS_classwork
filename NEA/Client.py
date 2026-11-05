'''
this class contains the high level game logic and also is used to direct the other classes to where they need to be used
the main point of this class is to act as a director and high level manager, so it doesn't use any pygame vectors or pygame logic
as that is handled by each class via their own internal methods
'''

import pygame

class Client:
    def __init__(self):

        #this is going to decide weather or not the game is in the room mode or in main menu mode
        self.mode = 'Menu'

        #the main list is going to store all objects in the game that can be modified by the client, e.g the player and all created objects
        self.mainList = []

        #main on/off state for the game so it knows when the player has quit
        self.running = True

        #making a time delta so all objects and moving things can move per frame
        self.dt = 60

        #adding a time clock so the time delta can be updated correctly
        self.clock = pygame.time.Clock()

        #this dictates whether key inputs for typing out a message or for movement
        self.typing = False

        #this is the message, and it gets cleared when it is sent
        self.message = ''

    def update_all(self, render):

        #updating the time delta so the players movement doesn't change with frame rate
        self.dt = self.clock.tick(60)/1000

        #going though all items in the main list and telling them to update themselves so they can be sent to the server or sent directly to the render list
        for item in self.mainList:
            if self.mode == 'Menu' and (item.type == 'B' or item.type == 'TDM'):
                item.update(render.renderList, self.dt, self.typing)
            elif self.mode == 'Game' and item.type != 'B':
                item.update(render.renderList, self.dt, self.typing)

        if len(self.message[self.message.rfind('\n')+1:]) >= 10:
            self.message += '\n'

    def flush_lists(self, lists):

        #here I am flushing all the lists that need to be flushed to prevent rapid RAM filling
        for item in lists:
            item.clear()

    def check_events(self):

        #doing the normal checks for a pygame instance to make sure it can be closed, and so I can check for things like pressing buttons
        for event in pygame.event.get():

            #searching though every event that has happened
            if event.type == pygame.QUIT:
                self.running = False

            #testing for a mouse button click and checking if we are in menu mode so that we can avoid unneeded checks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in self.mainList:
                    if event.button == 1:

                        #differing the menu and game button modes so that pressing an overlapping button won't crash the game
                        if self.mode == 'Menu' and item.type == 'B':

                            #checking if the event position where the mouse button was pressed was in a button
                            if item.rect.collidepoint(event.pos):
                                item.pressed(self)

                        elif self.mode == 'Game' and item.type == 'CB':

                            #checking if the event position where the mouse button was pressed was in a button
                            if item.rect.collidepoint(event.pos):
                                item.pressed(self)

            if event.type == pygame.KEYDOWN and self.typing:
                if event.key == pygame.K_BACKSPACE:
                    if self.message[len(self.message)-1:] == '\n':
                        self.message = self.message[:-2]
                    else:
                        self.message = self.message[:-1]

                elif event.key == pygame.K_RETURN and self.typing:
                    self.message = ''
                    self.typing = False
                else:
                    self.message += event.unicode