'''

this is the main game render class and file, this is separate so as to limit the amount of code in the client file and class.

the main idea for this class is that it will work as the main screen for each client and will handle most of the rendering and each item to be
rendered will have to inject themselves into the render list in this file so as to get rendered during the render phase of the main game loop.

the reason each class will have its own injection method will be that some items need to be sent first to the server so that they can be
sent to other players and used, or they just need to be sent directly to the main render list. like can be seen with the objects that the
player draws before confirming there placement

'''


import pygame
#importing pygame so it can be used to create the game instance in the render

class Render:
    def __init__(self):
        #this is the creation of the main render list that stores all info about the items to be rendered including
        self.renderList = []
        #this is the main screen for each client
        self.screen = pygame.display.set_mode((800, 600))

    def render(self):
        #this is where the render list gets iterated though to create the objects on the screen
        for item in self.renderList:
            #this is where the objects get tested and then drawn based of there type attribute
            if item[0] == True:
                pygame.draw.rect(self.screen, item[1], item[2])
            else:
                pygame.draw.ellipse(self.screen, item[1], item[2])
        #then update the screen made in the render class
        pygame.display.flip()