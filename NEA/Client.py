'''
this class contains the high level game logic and also is used to direct the other classes to where they need to be used
the main point of this class is to act as a director and high level manager, so it doesn't use any pygame vectors or pygame logic
as that is handled by each class via their own internal methods
'''

import pygame
from DrawElipse import DrawElipse
from DrawnObjectBase import DrawnObjectBase

class Client:
    def __init__(self):

        #this is going to decide weather or not the game is in the room mode or in main menu mode
        self.mode = 'Menu'

        #the main list is going to store all objects in the game that can be modified by the client, e.g the player and all created objects
        self.mainList = []

        self.sendToServer = []

        self.objectBeingDrawn = None

        #main on/off state for the game so it knows when the player has quit
        self.running = True

        #making a time delta so all objects and moving things can move per frame
        self.dt = 60

        #adding a time clock so the time delta can be updated correctly
        self.clock = pygame.time.Clock()

        #this dictates whether key inputs for typing out a message or for movement
        self.typing = False

        self.drawing = False

        #this is the message, and it gets cleared when it is sent
        self.message = ''

    def update_all(self, render):

        #updating the time delta so the players movement doesn't change with frame rate
        self.dt = self.clock.tick(60)/1000

        #going though all items in the main list and telling them to update themselves so they can be sent to the server or sent directly to the render list
        for item in self.mainList:
            if self.mode == 'Menu' and (item.type == 'B' or item.type == 'TDM'):
                item.update(self.sendToServer, self.dt, self.typing, pygame.mouse.get_pos())
            elif self.mode == 'Game' and (item.type == 'CB' or item.type == 'TD' or item.type == 'E' or item.type == 'R'):
                item.update(self.sendToServer, self.dt, self.typing, pygame.mouse.get_pos())

        if len(self.message[self.message.rfind('|')+1:]) >= 10:
            self.message += '|'

        render.renderList = self.sendToServer

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # checking whether the player has clicked a button
                    buttonPressed = False

                    for item in self.mainList:
                        if item.type in ('B', 'CB') and item.rect.collidepoint(event.pos):

                            # only allowing buttons in the current mode to be pressed
                            if (self.mode == 'Menu' and item.type == 'B') or (self.mode == 'Game' and item.type == 'CB'):
                                item.pressed(self)
                                buttonPressed = True
                                break

                    # only drawing objects when the player is in game mode
                    if not buttonPressed and self.mode == 'Game':

                        if not self.drawing:
                            self.objectBeingDrawn = DrawElipse(event.pos, event.pos, self)
                            self.drawing = True

                        else:
                            newObject = DrawnObjectBase(self,self.objectBeingDrawn.pos,self.objectBeingDrawn.type,self.objectBeingDrawn.colour,self.objectBeingDrawn.rect.copy())

                            # removing the temporary drawing object
                            self.mainList.remove(self.objectBeingDrawn)
                            self.objectBeingDrawn = None
                            self.drawing = False

            if event.type == pygame.KEYDOWN and self.drawing:

                # checking if the player wants to cancel the current drawing
                if event.key == pygame.K_ESCAPE:

                    # removing the temporary object from the main list
                    if self.objectBeingDrawn is not None:
                        self.mainList.remove(self.objectBeingDrawn)

                    # clearing the object reference and drawing state
                    self.objectBeingDrawn = None
                    self.drawing = False

            if event.type == pygame.KEYDOWN and self.typing:

                #performing checks for key edge cases and also checking for length of string so I can add a \n
                if event.key == pygame.K_BACKSPACE:
                    if self.message[len(self.message)-1:] == '|':
                        self.message = self.message[:-2]
                    else:
                        self.message = self.message[:-1]

                elif event.key == pygame.K_RETURN:
                    self.message = ''
                    self.typing = False

                else:
                    self.message += event.unicode