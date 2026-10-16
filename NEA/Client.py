'''
this class continents the high level game logic and also is used to direct the other classes to where they need to be used
the main point of this class is to act as a director and high level manager, so it doesn't use any pygame vectors or pygame logic
as that is handled by each class via their own internal methods
'''
import pygame


class Client:
    def __init__(self):

        #the main list is going to store all objects in the game that can be modified by the client, e.g the player and all created objects
        self.mainList = []

        #main on/off state for the game so it knows when the player has quit
        self.running = True

        #making a time delta so all objects and moving things can move per frame
        self.dt = 60

        #adding a time clock so the time delta can be updated correctly
        self.clock = pygame.time.Clock()

    def update_all(self, render):

        #going though all items in the main list and telling them to update themselves so they can be sent to the server or sent directly to the render list
        for item in self.mainList:
            item.update(render.renderList, self.dt)

        self.dt = self.clock.tick(60)/1000

    def flush_lists(self, lists):

        #here i am flushing all the lists that need to be flushed to prevent rapid RAM filling
        for item in lists:
            item.clear()

    def check_events(self):

        #doing the normal checks for a pygame instance to make sure it can be closed and so i can check for things like pressing buttons
        for event in pygame.event.get():

            #searching though every event that has happened
            if event.type == pygame.QUIT:
                self.running = False