'''
this class continents the high level game logic and also is used to direct the other classes to where they need to be used
the main point of this class is to act as a director and high level manager, so it doesn't use any pygame vectors or pygame logic
as that is handled by each class via their own internal methods
'''

from Render import Render
render = Render()
#here we are importing the render object and using it to make a instant of the renderer

class Client:
    def __init__(self):
        #the main list is going to store all objects in the game that can be modified by the client, e.g the player and all created objects
        self.mainList = []
        #main on/off state for the game so it knows when the player has quit
        self.running = True

    def update_all(self):
        #going though all items in the main list and telling them to update themselves so they can be sent to the server or sent directly to the render list
        for item in self.mainList:
            item.update(render.renderList)

    def flush_lists(self, lists):
        #here i am flushing all the lists that need to be flushed to prevent rapid RAM filling
        for item in lists:
            item = []

    def game_loop(self):
        #this is the code that will get exacted every game loop cycle 
        self.update_all()
        self.flush_lists([render.renderList])

